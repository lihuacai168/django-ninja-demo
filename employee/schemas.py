from datetime import date
from ninja import Schema
from common.schema import BaseSchemaOut


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(EmployeeIn):
    id: int

