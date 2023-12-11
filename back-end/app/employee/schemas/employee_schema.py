from datetime import datetime
from typing import Literal
from enum import IntEnum
from pydantic import BaseModel, EmailStr
from bson.objectid import ObjectId

class EmployeeTypeEnum(IntEnum):
    REGULAR = 0
    CONTRACTUAL = 1

class EmployeeBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    emp_type: EmployeeTypeEnum

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

class CreateRegularEmployeeSchema(EmployeeBaseSchema):
    emp_type: Literal[EmployeeTypeEnum.REGULAR]
    number_of_leaves: int
    benefits: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class CreateContractualEmployeeSchema(EmployeeBaseSchema):
    emp_type: Literal[EmployeeTypeEnum.CONTRACTUAL]
    contract_end_date: datetime
    project: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UpdateRegularEmployeeSchema(EmployeeBaseSchema):
    emp_type: Literal[EmployeeTypeEnum.REGULAR]
    number_of_leaves: int
    benefits: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

class UpdateContractualEmployeeSchema(EmployeeBaseSchema):
    emp_type: Literal[EmployeeTypeEnum.CONTRACTUAL]
    contract_end_date: datetime
    project: str

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

