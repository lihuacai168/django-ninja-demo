from enum import IntEnum
from typing import TypeVar, Generic, List, Optional
from ninja import Schema
from pydantic import conint, validator, BaseModel, Field
from pydantic.generics import GenericModel


class ErrorMsg(BaseModel):
    message: Optional[str] = None
    success: bool = True


GenericResultsType = TypeVar("GenericResultsType")


class StandResponse(ErrorMsg, GenericModel, Generic[GenericResultsType]):
    data: GenericResultsType


class DictId(BaseModel):
    id: conint(ge=-1)


class PageSchema(GenericModel, Generic[GenericResultsType]):
    total: int
    page_size: int
    page_index: int
    details: List[GenericResultsType]


class PageFilter(Schema):
    page_index: int = 1
    page_size: conint(ge=1, le=100) = 10
    ordering: str = Field("", alias="ordering", description="排序字段，多个时用,分割")

    @validator("page_index")
    def page_index_check(cls, page_index):
        if page_index <= 1:
            return 1
        return page_index  # pragma: no cover

    def dict(
        self,
        *,
        exclude_none=True,
        exclude={"page_index", "page_size", "ordering"},
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
    ) -> "DictStrAny":
        return super().dict(
            exclude_none=exclude_none,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
        )
