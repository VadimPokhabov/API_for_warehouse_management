from typing import List

from pydantic import BaseModel


class ExceptionSchema(BaseModel):
    """Basic Exception Scheme."""
    detail: str


class ExceptionValidationFieldSchema(BaseModel):
    """Exception Check Field Schema."""
    field: str = 'field name'
    message: str = 'message error'


class ExceptionValidationSchema(BaseModel):
    """Basic Exception Checking Scheme."""
    detail: List[ExceptionValidationFieldSchema]
