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

# @router.post("/employees", response=StandResponse[Union[DictId, None]])
# def create_employee(request, payload: EmployeeIn):
#     logger.info(f"input: payload={payload.dict()}")
#     return employee_service_impl.create_obj(payload, "huacai")
#
#
# @router.get(
#     "/employees/{employee_id}", response=StandResponse[Union[EmployeeOut, None]]
# )
# def get_employee(request, employee_id: int):
#     return employee_service_impl.get_obj(employee_id)
#
#
# @router.get("/employees", response=StandResponse[PageSchema[EmployeeOut]])
# def list_employees(request, filters: EmployeeFilters = Query(...)):
#     logger.info(f"input: filters={filters.dict()}")
#     objs = employee_service_impl.list_obj(filters, EmployeeOut)
#     return StandResponse(data=objs)
#
#
# @router.put("/employees/{employee_id}", response=StandResponse[Union[DictId, None]])
# def update_employee(request, employee_id: int, payload: EmployeeIn):
#     payload.department_id = employee_id
#     logger.info(f"input: payload={payload.dict()}")
#     return employee_service_impl.update_obj(employee_id, payload, "huacai")
#
#
# @router.delete("/employees/{employee_id}", response=StandResponse[bool])
# def delete_employee(request, employee_id: int):
#     return employee_service_impl.delete_obj(employee_id)
