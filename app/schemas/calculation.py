from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from app.models.calculation import OperationType

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: OperationType
    user_id: Optional[int] = None

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v):
        valid = {e.value for e in OperationType}
        if v not in valid:
            raise ValueError(f"type must be one of {sorted(valid)}")
        return v

    @model_validator(mode="after")
    def check_no_division_by_zero(self):
        if self.type == OperationType.DIVIDE and self.b == 0:
            raise ValueError("Divisor 'b' cannot be zero for Divide operations.")
        return self

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: OperationType
    result: Optional[float] = None
    user_id: Optional[int] = None

    model_config = {"from_attributes": True}
