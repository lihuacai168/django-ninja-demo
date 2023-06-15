from typing import Any, Optional

from ninja import Schema
from pydantic import conint


class BaseSchemaOut(Schema):
    err_code: conint(ge=0)
    err_msg: str
    data: Optional[Any]


class Message(Schema):
    details: str


