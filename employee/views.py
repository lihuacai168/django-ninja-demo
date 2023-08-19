"""员工curd view"""
import logging
from typing import Optional, Union

from ninja import Query, Router, Schema
from pydantic.fields import Field
from pydantic.types import conint

from core.schemas import DictId, PageSchema, StandResponse
from employee.employee_service_impl import employee_service_impl
from employee.schemas import EmployeeFilters, EmployeeIn, EmployeeOut

router = Router(tags=["employees"])

logger = logging.getLogger(__name__)


class Filters(Schema):
    first_name__contains: str = Field(None, alias="fisrt_name")
    last_name__contains: str = Field(None, alias="last_name")
    department_id: Optional[conint(ge=0)]


@router.post("/employees", response=StandResponse[Union[DictId, None]])
def create_employee(request, payload: EmployeeIn):
    logger.info(f"input: payload={payload.dict()}")
    return employee_service_impl.create_obj(payload, "huacai")


@router.get(
    "/employees/{employee_id}", response=StandResponse[Union[EmployeeOut, None]]
)
def get_employee(request, employee_id: int):
    return employee_service_impl.get_obj(employee_id)


@router.get("/employees", response=StandResponse[PageSchema[EmployeeOut]])
def list_employees(request, filters: EmployeeFilters = Query(...)):
    logger.info(f"input: filters={filters.dict()}")
    objs = employee_service_impl.list_obj(filters, EmployeeOut)
    return StandResponse(data=objs)


@router.put("/employees/{employee_id}", response=StandResponse[Union[DictId, None]])
def update_employee(request, employee_id: int, payload: EmployeeIn):
    payload.department_id = employee_id
    logger.info(f"input: payload={payload.dict()}")
    return employee_service_impl.update_obj(employee_id, payload, "huacai")


@router.delete("/employees/{employee_id}", response=StandResponse[bool])
def delete_employee(request, employee_id: int):
    return employee_service_impl.delete_obj(employee_id)
