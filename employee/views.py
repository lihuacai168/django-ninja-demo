"""employee curd view"""
import logging
from typing import Optional

from ninja import Schema
from ninja_jwt.authentication import JWTAuth
from pydantic.fields import Field
from pydantic.types import conint

from core.router import CRUDRouter
from employee.employee_service_impl import employee_service_impl
from employee.schemas import EmployeeFilters, EmployeeIn, EmployeeOut


logger = logging.getLogger(__name__)


class Filters(Schema):
    first_name__contains: str = Field(None, alias="first_name")
    last_name__contains: str = Field(None, alias="last_name")
    department_id: Optional[conint(ge=0)]


# CRUDRouter, like DRF model views set
router = CRUDRouter(
    service_impl=employee_service_impl,
    filters_class=EmployeeFilters,
    in_schema=EmployeeIn,
    out_schema=EmployeeOut,
    path="/employees",
    tags=["employees"],
    auth=JWTAuth()
)
