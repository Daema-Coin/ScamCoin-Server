from fastapi import APIRouter, Depends, Query
from fastapi_jwt_auth import AuthJWT

from domain.user.dto import GetUserCoinResponse, LoginRequest
from domain.user.service import user_login
from util import get_current_user

user_router = APIRouter(prefix="/user")


@user_router.post('/login')
def login(
        request: LoginRequest,
        auth: AuthJWT = Depends()
):
    return user_login(request.account_id, request.password, auth)


@user_router.get('/coin')
def get_user_coin(auth: AuthJWT = Depends()):
    user = get_current_user(auth)
    return GetUserCoinResponse(
        coin=user.coin_balance
    )
