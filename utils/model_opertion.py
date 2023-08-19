import logging
from typing import TypeVar, Union, Any
import traceback

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from pydantic import conint

from core.schemas import StandResponse, DictId
from core.model import CoreModel

logger = logging.getLogger(__name__)

GenericPayload = TypeVar("GenericPayload")


def create(creator: str, model: CoreModel, payload: GenericPayload) -> StandResponse[Union[DictId, None]]:
    """创建对象"""
    try:
        logger.info(f"input: create={model.__name__}, payload={payload.dict()}")
        obj = model.objects.create(creator=creator, **payload.dict())
    except Exception as e:
        logger.error(traceback.format_exc())
        return StandResponse(success=False, message=str(e), data=None)
    logger.info(f"create {model.__name__} success, id: {obj.id}")
    return StandResponse(data=DictId(id=obj.id))


def create_obj_with_validate_unique(
    creator: str,
    model: CoreModel,
    payload: GenericPayload,
    exclude: Any = None
) -> StandResponse[Union[DictId, dict]]:
    """创建对象，并且验证唯一性"""
    obj = model(
        creator=creator,
        **payload.dict()
    )
    try:
        logger.info(f"input: create={model.__name__}, payload={payload.dict()}")
        obj.validate_unique(exclude=exclude)
        obj.save()
    except ValidationError as e:
        logger.warning(traceback.format_exc())
        raise e

    logger.info(f"create {model.__name__} success, id: {obj.id}")
    return StandResponse(data=DictId(id=obj.id))


def _update(obj, payload: dict, updater: str) -> StandResponse[Union[DictId,None]]:
    logger.info(f"input: update={obj.__class__.__name__}, payload={payload}")
    obj.updater = updater
    for attr, value in payload.items():
        setattr(obj, attr, value)
    try:
        obj.save()
    except Exception as e:
        logger.warning(traceback.format_exc())
        return StandResponse(success=False, message=str(e), data=None)
    logger.info(f"update {obj.__class__.__name__} success, id: {obj.id}")
    return StandResponse(data=DictId(id=obj.id))


def update(updater: str, model: CoreModel, payload: GenericPayload, obj_id: conint(ge=1)) -> StandResponse[Union[DictId, None]]:
    """更新对象"""
    obj = get_object_or_404(model, id=obj_id)
    return _update(obj=obj, payload=payload.dict(), updater=updater)


def partial_update(updater: str, model: CoreModel, obj_id: conint(ge=1), **kwargs) -> StandResponse[Union[DictId, None]]:
    obj = get_object_or_404(model, id=obj_id)
    return _update(obj=obj, payload=kwargs, updater=updater)


def update_by_obj(obj: CoreModel, updater: str, **kwargs) -> StandResponse[Union[DictId, None]]:
    return _update(obj=obj, payload=kwargs, updater=updater)
