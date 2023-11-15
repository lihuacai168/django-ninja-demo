from datetime import date
from typing import Optional

from ninja import Schema
from pydantic import Field, conint

from core.schemas import PageFilter


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(EmployeeIn):
    id: int


class EmployeeFilters(PageFilter):
    first_name__contains: str = Field(None, alias="first_name")
    last_name__contains: str = Field(None, alias="last_name")
    department_id: Optional[conint(ge=0)]
