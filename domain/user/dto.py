from pydantic import BaseModel

from domain.user.model import User


class GetUserCoinResponse(BaseModel):
    coin: int


class TokenResponse(BaseModel):
    token: str


class LoginRequest(BaseModel):
    account_id: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    gcn: str
    coin_balance: int

    class Config:
        orm_mode = True


class GetUsersResponse(BaseModel):
    users: list[UserResponse]
