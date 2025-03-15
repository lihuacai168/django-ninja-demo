import logging
from typing import TypeVar, Union, Any, Optional, Dict, Type
import traceback

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from pydantic import conint

from core.schemas import StandResponse, DictId, OptionalDictResponseType
from core.model import CoreModel

logger = logging.getLogger(__name__)

GenericPayload = TypeVar("GenericPayload")

class ModelOperationLogger:
    @staticmethod
    def log_create_input(model_name: str, payload: Dict) -> None:
        logger.info(f"input: create={model_name}, payload={payload}")
        
    @staticmethod
    def log_create_success(model_name: str, obj_id: int) -> None:
        logger.info(f"create {model_name} success, id: {obj_id}")
        
    @staticmethod
    def log_create_error(error: Exception) -> None:
        logger.error(traceback.format_exc())
        
    @staticmethod
    def log_update_input(model_name: str, payload: Dict) -> None:
        logger.info(f"input: update={model_name}, payload={payload}")
        
    @staticmethod
    def log_update_success(model_name: str, obj_id: int) -> None:
        logger.info(f"update {model_name} success, id: {obj_id}")
        
    @staticmethod
    def log_update_error(error: Exception) -> None:
        logger.warning(traceback.format_exc())

class ModelOperationHelper:
    @staticmethod
    def get_object_by_id(model: Type[CoreModel], obj_id: int) -> CoreModel:
        return get_object_or_404(model, id=obj_id)
    
    @staticmethod
    def create_object(model: Type[CoreModel], **kwargs) -> CoreModel:
        return model.objects.create(**kwargs)
    
    @staticmethod
    def validate_unique(obj: CoreModel, exclude: Any = None) -> None:
        obj.validate_unique(exclude=exclude)
        
    @staticmethod
    def save_object(obj: CoreModel) -> None:
        obj.save()
        
    @staticmethod
    def update_object_attrs(obj: CoreModel, **attrs) -> None:
        for attr, value in attrs.items():
            setattr(obj, attr, value)

class ModelOperation:
    def __init__(self, logger: ModelOperationLogger = None, helper: ModelOperationHelper = None):
        self.logger = logger or ModelOperationLogger()
        self.helper = helper or ModelOperationHelper()
    
    def create(self, creator: str, model: Type[CoreModel], payload: GenericPayload) -> StandResponse[Optional[DictId]]:
        """创建对象"""
        try:
            payload_dict = payload.dict()
            self.logger.log_create_input(model.__name__, payload_dict)
            
            obj = self.helper.create_object(model, creator=creator, **payload_dict)
            
            self.logger.log_create_success(model.__name__, obj.id)
            return StandResponse[Optional[DictId]](data=DictId(id=obj.id))
        except Exception as e:
            self.logger.log_create_error(e)
            return StandResponse[Optional[DictId]](success=False, message=str(e), data=None)

    def create_obj_with_validate_unique(
        self,
        creator: str,
        model: Type[CoreModel],
        payload: GenericPayload,
        exclude: Any = None
    ) -> StandResponse[Union[DictId, dict]]:
        """创建对象，并且验证唯一性"""
        payload_dict = payload.dict()
        self.logger.log_create_input(model.__name__, payload_dict)
        
        obj = model(creator=creator, **payload_dict)
        
        try:
            self.helper.validate_unique(obj, exclude=exclude)
            self.helper.save_object(obj)
            
            self.logger.log_create_success(model.__name__, obj.id)
            return StandResponse[Union[DictId, dict]](data=DictId(id=obj.id))
        except ValidationError as e:
            self.logger.log_create_error(e)
            raise e

    def _update(self, obj: CoreModel, payload: dict, updater: str) -> OptionalDictResponseType:
        self.logger.log_update_input(obj.__class__.__name__, payload)
        
        try:
            obj.updater = updater
            self.helper.update_object_attrs(obj, **payload)
            self.helper.save_object(obj)
            
            self.logger.log_update_success(obj.__class__.__name__, obj.id)
            return OptionalDictResponseType(data=DictId(id=obj.id))
        except Exception as e:
            self.logger.log_update_error(e)
            return OptionalDictResponseType(success=False, message=str(e), data=None)

    def update(self, updater: str, model: Type[CoreModel], payload: GenericPayload, obj_id: conint(ge=1)) -> StandResponse[Union[DictId, None]]:
        """更新对象"""
        obj = self.helper.get_object_by_id(model, obj_id)
        return self._update(obj=obj, payload=payload.dict(), updater=updater)

    def partial_update(self, updater: str, model: Type[CoreModel], obj_id: conint(ge=1), **kwargs) -> OptionalDictResponseType:
        obj = self.helper.get_object_by_id(model, obj_id)
        return self._update(obj=obj, payload=kwargs, updater=updater)

    def update_by_obj(self, obj: CoreModel, updater: str, **kwargs) -> OptionalDictResponseType:
        return self._update(obj=obj, payload=kwargs, updater=updater)

# 创建全局实例以保持向后兼容性
model_operation = ModelOperation()

# 导出函数以保持向后兼容性
create = model_operation.create
create_obj_with_validate_unique = model_operation.create_obj_with_validate_unique
update = model_operation.update
partial_update = model_operation.partial_update
update_by_obj = model_operation.update_by_obj
