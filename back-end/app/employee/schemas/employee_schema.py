from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class EmployeeBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    emp_type: int
    number_of_leaves: int | None = None
    benefits: str | None = None
    contract_end_date: datetime | None = None
    project: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

class CreateEmployeeSchema(EmployeeBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    verified: bool = False

class UpdateEmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    emp_type: int
    number_of_leaves: int | None = None
    benefits: str | None = None
    contract_end_date: datetime | None = None
    project: str | None = None

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
