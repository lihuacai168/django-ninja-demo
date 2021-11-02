from typing import List, Optional
from ninja import Router, Query, Schema
from django.shortcuts import get_object_or_404
from pydantic.fields import Field
from pydantic.types import conint



from common.schema import Message
from employee.models import Employee
from employee.schemas import EmployeeIn, EmployeeOut

router = Router(tags=['employees'])


class Filters(Schema):
    first_name__contains: str = Field(None, alias="fisrt_name")
    last_name__contains: str = Field(None, alias="last_name")
    department_id: Optional[conint(ge=0)]


@router.post("/employees")
def create_employee(request, payload: EmployeeIn):
    employee = Employee.objects.create(**payload.dict())
    return {"id": employee.id}


@router.get("/employees/{employee_id}", response={200: EmployeeOut, 404: Message})
def get_employee(request, employee_id: int):
    """
    - :param employee_id:
    - :return:
        - 200返回正常
        - 404找不到对象
    """
    employee = get_object_or_404(Employee, id=employee_id)
    return employee


@router.get("/employees", response=List[EmployeeOut])
def list_employees(request, filters: Filters = Query(...)):
    qs = Employee.objects.filter(**filters.dict(exclude_none=True))
    print(qs.query)
    return qs


@router.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for attr, value in payload.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": True}


@router.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}
