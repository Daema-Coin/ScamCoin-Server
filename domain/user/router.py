from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.user.dto import GetUserCoinResponse, LoginRequest, GetUsersResponse, UserResponse
from domain.user.model import User
from domain.user.service import user_login
from util import get_current_user, check_is_admin

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


@user_router.get('/')
def get_users(auth: AuthJWT = Depends()):
    check_is_admin(auth)
    users = [UserResponse.from_orm(user) for user in session.query(User).all()]
    return GetUsersResponse(users=users)
