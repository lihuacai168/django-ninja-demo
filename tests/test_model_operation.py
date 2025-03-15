from django.test import TestCase
from django.core.exceptions import ValidationError
from django.http import Http404
from django.db import models
from pydantic import BaseModel
from employee.models import Employee, Department
from utils.model_opertion import (
    ModelOperation,
    ModelOperationLogger,
    ModelOperationHelper,
    create, 
    create_obj_with_validate_unique,
    update,
    partial_update,
    update_by_obj,
)

class EmployeePayload:
    def __init__(self, **kwargs):
        self.data = kwargs
        
    def dict(self):
        return self.data

class TestModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creator = models.CharField(max_length=100)
    updater = models.CharField(max_length=100, null=True)
    
    class Meta:
        app_label = 'employee'

class TestPayload(BaseModel):
    name: str

class SaveErrorModel(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    updater = models.CharField(max_length=100, null=True)
    
    def save(self, *args, **kwargs):
        raise ValidationError("Test save error")
    
    class Meta:
        app_label = 'employee'

class TestModelOperationLogger(TestCase):
    def setUp(self):
        self.logger = ModelOperationLogger()
        
    def test_log_create_input(self):
        with self.assertLogs('utils.model_opertion', level='INFO') as cm:
            self.logger.log_create_input('Employee', {'name': 'John'})
            self.assertIn('input: create=Employee, payload={\'name\': \'John\'}', cm.output[0])
            
    def test_log_create_success(self):
        with self.assertLogs('utils.model_opertion', level='INFO') as cm:
            self.logger.log_create_success('Employee', 1)
            self.assertIn('create Employee success, id: 1', cm.output[0])
            
    def test_log_create_error(self):
        with self.assertLogs('utils.model_opertion', level='ERROR') as cm:
            self.logger.log_create_error(Exception('test error'))
            self.assertIn('test error', cm.output[0])
            
    def test_log_update_input(self):
        with self.assertLogs('utils.model_opertion', level='INFO') as cm:
            self.logger.log_update_input('Employee', {'name': 'John'})
            self.assertIn('input: update=Employee, payload={\'name\': \'John\'}', cm.output[0])
            
    def test_log_update_success(self):
        with self.assertLogs('utils.model_opertion', level='INFO') as cm:
            self.logger.log_update_success('Employee', 1)
            self.assertIn('update Employee success, id: 1', cm.output[0])
            
    def test_log_update_error(self):
        with self.assertLogs('utils.model_opertion', level='WARNING') as cm:
            self.logger.log_update_error(Exception('test error'))
            self.assertIn('test error', cm.output[0])

class TestModelOperationHelper(TestCase):
    def setUp(self):
        self.helper = ModelOperationHelper()
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            creator='test'
        )
        
    def test_get_object_by_id(self):
        obj = self.helper.get_object_by_id(Employee, self.employee.id)
        self.assertEqual(obj.id, self.employee.id)
        
    def test_get_object_by_id_not_found(self):
        with self.assertRaises(Http404):
            self.helper.get_object_by_id(Employee, 999)
            
    def test_create_object(self):
        obj = self.helper.create_object(
            Employee,
            first_name='Jane',
            last_name='Doe',
            creator='test'
        )
        self.assertEqual(obj.first_name, 'Jane')
        
    def test_validate_unique(self):
        obj = Employee(
            first_name='John',
            last_name='Doe',
            creator='test'
        )
        with self.assertRaises(ValidationError):
            self.helper.validate_unique(obj)
            
    def test_save_object(self):
        obj = Employee(
            first_name='Jane',
            last_name='Smith',
            creator='test'
        )
        self.helper.save_object(obj)
        self.assertIsNotNone(obj.id)
        
    def test_save_object_error(self):
        obj = SaveErrorModel(name='test', creator='test')
        with self.assertRaises(ValidationError):
            self.helper.save_object(obj)
            
    def test_update_object_attrs(self):
        self.helper.update_object_attrs(
            self.employee,
            first_name='Jane',
            last_name='Smith'
        )
        self.assertEqual(self.employee.first_name, 'Jane')
        self.assertEqual(self.employee.last_name, 'Smith')

class TestModelOperation(TestCase):
    def setUp(self):
        self.mock_logger = Mock(spec=ModelOperationLogger)
        self.mock_helper = Mock(spec=ModelOperationHelper)
        self.model_operation = ModelOperation(
            logger=self.mock_logger,
            helper=self.mock_helper
        )
        
    def test_create_success(self):
        payload = EmployeePayload(first_name='John', last_name='Doe')
        mock_obj = Mock(id=1)
        self.mock_helper.create_object.return_value = mock_obj
        
        result = self.model_operation.create('test', Employee, payload)
        
        self.mock_logger.log_create_input.assert_called_once_with('Employee', payload.dict())
        self.mock_helper.create_object.assert_called_once_with(
            Employee,
            creator='test',
            first_name='John',
            last_name='Doe'
        )
        self.mock_logger.log_create_success.assert_called_once_with('Employee', 1)
        self.assertTrue(result.success)
        self.assertEqual(result.data.id, 1)
        
    def test_create_error(self):
        payload = EmployeePayload(first_name='John', last_name='Doe')
        error = Exception('test error')
        self.mock_helper.create_object.side_effect = error
        
        result = self.model_operation.create('test', Employee, payload)
        
        self.mock_logger.log_create_error.assert_called_once_with(error)
        self.assertFalse(result.success)
        self.assertEqual(result.message, 'test error')
        
    def test_create_obj_with_validate_unique_success(self):
        payload = EmployeePayload(first_name='John', last_name='Doe')
        mock_obj = Mock(id=1)
        self.mock_helper.save_object.return_value = None
        
        result = self.model_operation.create_obj_with_validate_unique('test', Employee, payload)
        
        self.mock_logger.log_create_input.assert_called_once_with('Employee', payload.dict())
        self.mock_helper.validate_unique.assert_called_once()
        self.mock_helper.save_object.assert_called_once()
        self.mock_logger.log_create_success.assert_called_once()
        self.assertTrue(result.success)
        
    def test_create_obj_with_validate_unique_error(self):
        payload = EmployeePayload(first_name='John', last_name='Doe')
        error = ValidationError('test error')
        self.mock_helper.validate_unique.side_effect = error
        
        with self.assertRaises(ValidationError):
            self.model_operation.create_obj_with_validate_unique('test', Employee, payload)
            
        self.mock_logger.log_create_error.assert_called_once_with(error)
        
    def test_create_obj_with_validate_unique_save_error(self):
        payload = EmployeePayload(first_name='John', last_name='Doe')
        error = ValidationError('test error')
        self.mock_helper.save_object.side_effect = error
        
        with self.assertRaises(ValidationError):
            self.model_operation.create_obj_with_validate_unique('test', Employee, payload)
            
        self.mock_logger.log_create_error.assert_called_once_with(error)
        
    def test_update_success(self):
        payload = EmployeePayload(first_name='Jane')
        mock_obj = Mock(id=1, __class__=Mock(__name__='Employee'))
        self.mock_helper.get_object_by_id.return_value = mock_obj
        
        result = self.model_operation.update('test', Employee, payload, 1)
        
        self.mock_helper.get_object_by_id.assert_called_once_with(Employee, 1)
        self.mock_logger.log_update_input.assert_called_once()
        self.mock_helper.update_object_attrs.assert_called_once()
        self.mock_helper.save_object.assert_called_once_with(mock_obj)
        self.mock_logger.log_update_success.assert_called_once()
        self.assertTrue(result.success)
        
    def test_update_error(self):
        payload = EmployeePayload(first_name='Jane')
        mock_obj = Mock(id=1, __class__=Mock(__name__='Employee'))
        self.mock_helper.get_object_by_id.return_value = mock_obj
        error = Exception('test error')
        self.mock_helper.save_object.side_effect = error
        
        result = self.model_operation.update('test', Employee, payload, 1)
        
        self.mock_logger.log_update_error.assert_called_once_with(error)
        self.assertFalse(result.success)
        self.assertEqual(result.message, 'test error')
        
    def test_update_get_object_error(self):
        payload = EmployeePayload(first_name='Jane')
        error = Http404('Not found')
        self.mock_helper.get_object_by_id.side_effect = error
        
        with self.assertRaises(Http404):
            self.model_operation.update('test', Employee, payload, 1)
        
    def test_partial_update(self):
        mock_obj = Mock(id=1, __class__=Mock(__name__='Employee'))
        self.mock_helper.get_object_by_id.return_value = mock_obj
        
        result = self.model_operation.partial_update('test', Employee, 1, first_name='Jane')
        
        self.mock_helper.get_object_by_id.assert_called_once_with(Employee, 1)
        self.mock_logger.log_update_input.assert_called_once()
        self.mock_helper.update_object_attrs.assert_called_once()
        self.mock_helper.save_object.assert_called_once_with(mock_obj)
        self.assertTrue(result.success)
        
    def test_partial_update_get_object_error(self):
        error = Http404('Not found')
        self.mock_helper.get_object_by_id.side_effect = error
        
        with self.assertRaises(Http404):
            self.model_operation.partial_update('test', Employee, 1, first_name='Jane')
        
    def test_update_by_obj(self):
        mock_obj = Mock(id=1, __class__=Mock(__name__='Employee'))
        
        result = self.model_operation.update_by_obj(mock_obj, 'test', first_name='Jane')
        
        self.mock_logger.log_update_input.assert_called_once()
        self.mock_helper.update_object_attrs.assert_called_once()
        self.mock_helper.save_object.assert_called_once_with(mock_obj)
        self.assertTrue(result.success)
        
    def test_update_by_obj_error(self):
        mock_obj = Mock(id=1, __class__=Mock(__name__='Employee'))
        error = ValidationError('test error')
        self.mock_helper.save_object.side_effect = error
        
        result = self.model_operation.update_by_obj(mock_obj, 'test', first_name='Jane')
        
        self.mock_logger.log_update_error.assert_called_once_with(error)
        self.assertFalse(result.success)
        self.assertEqual(result.message, 'test error')

class TestModelOperationCompatibility(TestCase):
    """测试向后兼容性函数"""
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            creator='test'
        )
        
    def test_create(self):
        payload = EmployeePayload(first_name='Jane', last_name='Smith')
        result = create('test', Employee, payload)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data.id)
        
    def test_create_error(self):
        payload = EmployeePayload(first_name='Jane', last_name='Smith', department_id=999)  # 不存在的department_id
        result = create('test', Employee, payload)
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        
    def test_create_obj_with_validate_unique(self):
        payload = EmployeePayload(
            first_name='John',  # 已存在的名字
            last_name='Doe'
        )
        with self.assertRaises(ValidationError):
            create_obj_with_validate_unique('test', Employee, payload)
            
    def test_create_obj_with_validate_unique_save_error(self):
        payload = EmployeePayload(name='test')
        with self.assertRaises(ValidationError):
            create_obj_with_validate_unique('test', SaveErrorModel, payload)
            
    def test_update(self):
        payload = EmployeePayload(first_name='Jane')
        result = update('test', Employee, payload, self.employee.id)
        self.assertTrue(result.success)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Jane')
        
    def test_update_not_found(self):
        payload = EmployeePayload(first_name='Jane')
        with self.assertRaises(Http404):
            update('test', Employee, payload, 999)
            
    def test_update_error(self):
        payload = EmployeePayload(name='test')
        obj = SaveErrorModel.objects.create(name='test', creator='test')
        result = update('test', SaveErrorModel, payload, obj.id)
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        
    def test_partial_update(self):
        result = partial_update('test', Employee, self.employee.id, first_name='Jane')
        self.assertTrue(result.success)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Jane')
        
    def test_partial_update_not_found(self):
        with self.assertRaises(Http404):
            partial_update('test', Employee, 999, first_name='Jane')
            
    def test_partial_update_error(self):
        obj = SaveErrorModel.objects.create(name='test', creator='test')
        result = partial_update('test', SaveErrorModel, obj.id, name='test2')
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        
    def test_update_by_obj(self):
        result = update_by_obj(self.employee, 'test', first_name='Jane')
        self.assertTrue(result.success)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Jane')
        
    def test_update_by_obj_error(self):
        obj = SaveErrorModel.objects.create(name='test', creator='test')
        result = update_by_obj(obj, 'test', name='test2')
        self.assertFalse(result.success)
        self.assertIsNone(result.data) 