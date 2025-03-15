from django.test import TestCase
from django.contrib.auth import get_user_model
from core.auth import (
    MyTokenObtainPairOutSchema,
    MyRefreshTokenOutSchema,
    MyTokenObtainPairInputSchema,
    MyTokenRefreshInputSchema,
    CustomAuthBackend,
    UserSchema
)
from typing import Dict, Union, Set

User = get_user_model()

class TestAuth(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test'
        )
        self.auth_backend = CustomAuthBackend()

    def test_my_refresh_token_out_schema_dict(self):
        # 测试MyRefreshTokenOutSchema的dict方法
        schema = MyRefreshTokenOutSchema(access="test_access", refresh="test_refresh")
        result = schema.dict()
        expected = {
            "data": {"access": "test_access", "refresh": "test_refresh"},
            "message": None,
            "success": True
        }
        self.assertEqual(result, expected)
        
        # 测试带有可选参数的dict方法
        result = schema.dict(
            include={"access"},  # type: ignore
            exclude={"refresh"},  # type: ignore
            by_alias=True,
            skip_defaults=True,
            exclude_unset=True,
            exclude_defaults=True,
            exclude_none=True
        )
        self.assertEqual(result, {
            "data": {"access": "test_access", "refresh": "test_refresh"},
            "message": None,
            "success": True
        })

    def test_my_token_obtain_pair_input_schema_get_token(self):
        # 测试MyTokenObtainPairInputSchema的get_token方法
        result = MyTokenObtainPairInputSchema.get_token(self.user)
        self.assertIn('data', result)
        self.assertIn('refresh', result['data'])
        self.assertIn('access', result['data'])
        self.assertIn('user', result['data'])
        self.assertEqual(result['data']['user'].first_name, 'Test')
        self.assertEqual(result['data']['user'].email, 'test@example.com')

    def test_custom_auth_backend_authenticate_success(self):
        # 测试CustomAuthBackend的authenticate方法 - 成功情况
        authenticated_user = self.auth_backend.authenticate(
            None,
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(authenticated_user, self.user)

    def test_custom_auth_backend_authenticate_wrong_password(self):
        # 测试CustomAuthBackend的authenticate方法 - 密码错误
        authenticated_user = self.auth_backend.authenticate(
            None,
            username='testuser',
            password='wrongpass'
        )
        self.assertIsNone(authenticated_user)

    def test_custom_auth_backend_authenticate_user_not_exist(self):
        # 测试CustomAuthBackend的authenticate方法 - 用户不存在
        authenticated_user = self.auth_backend.authenticate(
            None,
            username='nonexistentuser',
            password='testpass123'
        )
        self.assertIsNone(authenticated_user)
        
    def test_user_schema(self):
        # 测试UserSchema
        user_schema = UserSchema(first_name="Test", email="test@example.com")
        self.assertEqual(user_schema.first_name, "Test")
        self.assertEqual(user_schema.email, "test@example.com")
        
    def test_my_token_obtain_pair_out_schema(self):
        # 测试MyTokenObtainPairOutSchema
        schema = MyTokenObtainPairOutSchema(
            refresh="test_refresh",
            access="test_access",
            user=UserSchema(first_name="Test", email="test@example.com")
        )
        self.assertEqual(schema.refresh, "test_refresh")
        self.assertEqual(schema.access, "test_access")
        self.assertEqual(schema.user.first_name, "Test")
        self.assertEqual(schema.user.email, "test@example.com")
        
    def test_my_token_obtain_pair_input_schema_get_response_schema(self):
        # 测试MyTokenObtainPairInputSchema的get_response_schema方法
        response_schema = MyTokenObtainPairInputSchema.get_response_schema()
        self.assertTrue(hasattr(response_schema, '__origin__'))
        
    def test_my_token_refresh_input_schema_get_response_schema(self):
        # 测试MyTokenRefreshInputSchema的get_response_schema方法
        response_schema = MyTokenRefreshInputSchema.get_response_schema()
        self.assertEqual(response_schema, MyRefreshTokenOutSchema) 