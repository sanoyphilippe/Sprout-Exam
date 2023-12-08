from pydantic import BaseModel, constr

class LoginUserSchema(BaseModel):
    username: str
    password: constr(min_length=8)
