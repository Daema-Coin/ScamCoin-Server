from pydantic import BaseModel


class GetUserCoinResponse(BaseModel):
    coin: int


class TokenResponse(BaseModel):
    token: str


class LoginRequest(BaseModel):
    account_id: str
    password: str
