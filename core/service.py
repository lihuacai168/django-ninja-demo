import uuid
from abc import ABC, abstractmethod
from typing import Any, Union

from django.db.models import Model
from django.http import Http404
from django.shortcuts import get_object_or_404

from core import cache, response
from core.model import CoreModelSoftDelete
from core.schemas import DictId, PageFilter, PageSchema, StandResponse
from utils import model_opertion
from utils.model_opertion import GenericPayload


class BaseCURD(ABC):
    @abstractmethod
    def create_obj(self, payload: GenericPayload) -> DictId:
        ...

    @abstractmethod
    def get_obj(self, id: int) -> Union[Model, None]:
        ...

    @abstractmethod
    def list_obj(self, page_filter: PageFilter) -> PageSchema:
        ...

    @abstractmethod
    def update_obj(
        self, id: int, payload: GenericPayload, user_email: str
    ) -> Union[DictId, dict]:
        ...

    def delete_obj(self, id: int) -> bool:
        ...

    def partial_update(
        self, id: int, user_email: str, **fields_kv
    ) -> Union[DictId, dict]:
        ...

    @staticmethod
    def query_or_cache(ttl: int, alias: str, key: str, func, *args, **kwargs):
        return cache.query_or_cache(ttl, alias, key, func, *args, **kwargs)

    @staticmethod
    def query_or_cache_default(func, key: str, *args, **kwargs):
        return cache.query_or_cache_default_10min(func, key, *args, **kwargs)

    @staticmethod
    def query_or_cache_ttl(func, key: str, ttl: int, *args, **kwargs):
        return cache.query_or_cache_default(func, key, ttl, *args, **kwargs)

    @staticmethod
    def execute_sql(sql: str, db_conn):
        with db_conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result


class GenericCURD(BaseCURD):
    def __init__(self, model):
        self.model = model

    def create_obj(self, payload, user_email) -> StandResponse[Union[DictId, dict]]:
        return model_opertion.create(
            model=self.model, payload=payload, creator=user_email
        )

    def get_obj(self, id: int) -> StandResponse:
        return StandResponse(data=get_object_or_404(self.model, id=id))

    def list_obj(self, page_filter: PageFilter, page_schema: PageSchema) -> PageSchema:
        qs = self.model.objects.filter(**page_filter.dict())
        return response.get_page(queryset=qs, pager_filter=page_filter, generic_result_type=page_schema)

    def update_obj(
        self, id: int, payload, user_email
    ) -> StandResponse[Union[DictId, dict]]:
        return model_opertion.update(
            updater=user_email, model=self.model, payload=payload, obj_id=id
        )

    def partial_update(self, id: int, user_email: str, **fields_kv):
        return model_opertion.partial_update(
            updater=user_email, model=self.model, obj_id=id, **fields_kv
        )

    def delete_obj(self, id: int) -> StandResponse[bool]:
        bot = get_object_or_404(self.model, id=id)
        bot.delete()
        return StandResponse[bool](data=True)


class GenericCURDSoftDelete(BaseCURD):
    def __init__(self, model: CoreModelSoftDelete):
        self.model = model

    def create_obj(self, payload, user_email) -> StandResponse[Union[DictId, dict]]:
        return model_opertion.create(
            model=self.model, payload=payload, creator=user_email
        )

    def create_obj_with_validate_unique(
        self,
        payload,
        user_email: str,
        exclude: Any = None,
    ) -> StandResponse[Union[DictId, dict]]:
        return model_opertion.create_obj_with_validate_unique(
            model=self.model,
            payload=payload,
            creator=user_email,
            exclude=exclude,
        )

    def _get_obj_by_id(self, id: int, is_deleted=0) -> Union[Model, None]:
        try:
            obj = get_object_or_404(self.model, id=id, is_deleted=is_deleted)
        except Http404:
            return None
        return obj

    def get_obj(self, id: int) -> StandResponse[Union[Model, None]]:
        return StandResponse(data=self._get_obj_by_id(id=id))

    def list_obj(self, page_filter: PageFilter, page_schema: PageSchema) -> PageSchema:
        qs = self.model.objects.filter(**page_filter.dict(), is_deleted=0)
        return response.get_page(queryset=qs, pager_filter=page_filter, generic_result_type=page_schema)

    def update_obj(
        self, id: int, payload: GenericPayload, user_email: str
    ) -> StandResponse[Union[DictId, None]]:
        obj = self._get_obj_by_id(id=id)
        if obj is None:
            return StandResponse[dict](message=f"{id=} not exist", success=False, data={})
        return model_opertion.update_by_obj(
            updater=user_email, obj=obj, **payload.dict()
        )

    def partial_update(self, id: int, user_email: str, **fields_kv) -> StandResponse[Union[DictId, None]]:
        obj = self._get_obj_by_id(id=id)
        return model_opertion.update_by_obj(updater=user_email, obj=obj, **fields_kv)

    def delete_obj(self, id: int) -> StandResponse[bool]:
        obj = self._get_obj_by_id(id=id)
        if obj is None:
            return StandResponse[bool](data=False, message=f"{id=} not exist")
        obj.is_deleted = str(uuid.uuid1())
        obj.save()
        return StandResponse[bool](data=True)

    def bulk_create(self, objs: list) -> list:
        return self.model.objects.bulk_create(objs)
