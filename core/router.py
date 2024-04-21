from typing import Any, List, Optional, Type, TypeVar, Union

from core.schemas import DictId, PageFilter, PageSchema, StandResponse
from core.service import GenericCURD
from ninja import Body, Query, Router, Schema
from ninja.constants import NOT_SET_TYPE

TPageFilter = TypeVar("TPageFilter", bound=PageFilter)
TSchema = TypeVar("TSchema", bound=Schema)


class CRUDRouter(Router):
    def __init__(
        self,
        service_impl: GenericCURD,
        filters_class: Type[TPageFilter],
        in_schema: Type[TSchema],
        out_schema: Type[TSchema],
        path: str = "",
        tags: Optional[List[str]] = None,
        auth: Any = NOT_SET_TYPE,
    ):
        super().__init__(tags=tags, auth=auth)
        self.service_impl = service_impl
        self.filters_class = filters_class
        self.in_schema = in_schema
        self.out_schema = out_schema
        self.path = path
        self.register_crud_routes()

    def register_crud_routes(self):
        # create an obj
        @self.post(self.path, response=StandResponse[Union[DictId, None]])
        def create_obj(request, payload: self.in_schema):
            return self.service_impl.create_obj(
                payload, request.user.username
            )

        # get an obj
        @self.get(
            f"{self.path}/{{id}}", response=StandResponse[Union[self.out_schema, None]]
        )
        def get_obj(request, id: int):
            return self.service_impl.get_obj(id)

        # get a list of objs
        @self.get(self.path, response=StandResponse[PageSchema[self.out_schema]])
        def list_obj(request, filters: self.filters_class = Query(...)):
            objs = self.service_impl.list_obj(filters, self.out_schema)
            return StandResponse(data=objs)

        # full update obj
        @self.put(
            f"{self.path}/{{id}}",
            response=StandResponse[Union[DictId, dict]],
            description="full obj update",
        )
        def update_obj(request, id: int, payload: self.in_schema):
            return self.service_impl.update_obj(
                id, payload, request.user.username
            )

        # partial update obj
        @self.patch(
            f"{self.path}/{{id}}",
            response=StandResponse[Union[DictId, None]],
            description="partial obj update",
        )
        def partial_update_obj(request, id: int, payload: dict = Body(...)):
            return self.service_impl.partial_update(
                id, request.user.username, **payload
            )

        # delete an obj
        @self.delete(f"{self.path}/{{id}}", response=StandResponse[bool])
        def delete_obj(request, id: int):
            return self.service_impl.delete_obj(id)
