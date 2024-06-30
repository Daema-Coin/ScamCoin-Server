from pydantic import BaseModel


class BoothLoginRequest(BaseModel):
    auth_code: str


class BoothLoginResponse(BaseModel):
    token: str
    is_admin: str
