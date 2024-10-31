from typing import TypeVar, Generic, List, Optional, Union
from ninja import Schema
from pydantic import conint, BaseModel, Field, field_validator


class ErrorMsg(BaseModel):
    message: Optional[str] = None
    success: bool = True


GenericResultsType = TypeVar("GenericResultsType")


class StandResponse(ErrorMsg, Generic[GenericResultsType]):
    data: GenericResultsType


class DictId(BaseModel):
    id: conint(ge=-1)


OptionalDictResponseType = StandResponse[Union[Optional[DictId], dict]]


class PageSchema(BaseModel, Generic[GenericResultsType]):
    total: int
    page_size: int
    page_index: int
    details: List[GenericResultsType]


class PageFilter(Schema):
    page_index: int = 1
    page_size: conint(ge=1, le=100) = 10
    ordering: str = Field("", alias="ordering", description="排序字段，多个时用,分割")

    @field_validator("page_index")
    def page_index_check(cls, page_index):
        if page_index <= 1:
            return 1
        return page_index  # pragma: no cover

    def dict(
        self,
        *,
        exclude_none=True,
        exclude=None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
    ) -> "DictStrAny":
        if exclude is None:
            exclude = {"page_index", "page_size", "ordering"}
        return super().dict(
            exclude_none=exclude_none,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
        )
