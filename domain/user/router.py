from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from domain.user.dto import GetUserCoinResponse
from util import get_current_user

user_router = APIRouter(prefix="/user")


@user_router.post('/login')
def user_login(type: str):
    pass


@user_router.get('/coin')
def get_user_coin(auth: AuthJWT = Depends()):
    user = get_current_user(auth)
    return GetUserCoinResponse(
        coin=user.coin_balance
    )
