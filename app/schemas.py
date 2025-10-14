from pydantic import BaseModel


class RegistertUser(BaseModel):
    email: str
    password: str


class LoginUser(RegistertUser):
    pass


class SearchUserByEmail(BaseModel):
    email: str

class FormRoofFirst(BaseModel):
    L: int | float
    b: int | float
    h: int | float
    q_s: int | float
    g_k: int | float
    g_u: int | float
    q_w: int | float
    q_dop: int | float
    E: int | float

class SearchUserById(BaseModel):
    id: int