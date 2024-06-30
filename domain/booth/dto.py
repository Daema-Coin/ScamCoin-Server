from pydantic import BaseModel


class BoothLoginRequest(BaseModel):
    auth_code: str


class BoothLoginResponse(BaseModel):
    token: str
    is_admin: str


class GetBoothInfoResponse(BaseModel):
    name: str
    profit: int

    class Config:
        orm_mode = True