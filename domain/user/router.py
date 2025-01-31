from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from database import get_db, transaction
from domain.user.dto import GetUserCoinResponse, LoginRequest, GetUsersResponse, UserResponse, GrantCoinRequest, \
    TokenResponse
from domain.user.model import User
from domain.user.service import user_login
from util import get_current_user, check_is_admin

user_router = APIRouter(prefix="/user")


@user_router.post(
    '/login',
    status_code=201,
    response_model=TokenResponse,
    description='학생 로그인'
)
def login(
        request: LoginRequest,
        auth: AuthJWT = Depends(),
        session=Depends(get_db),
):
    return user_login(request.account_id, request.password, auth, session)


@user_router.get(
    '/coin',
    response_model=GetUserCoinResponse,
    description='내 코인 잔액 조회'
)
def get_user_coin(auth: AuthJWT = Depends(), session=Depends(get_db)):
    user = get_current_user(auth, session)
    return GetUserCoinResponse(
        coin=user.coin_balance
    )


@user_router.post(
    '/coin',
    status_code=204,
    description='코인 부여'
)
def grant_coin(request: GrantCoinRequest, auth: AuthJWT = Depends(), session=Depends(get_db)):
    with transaction(session):
        check_is_admin(auth, session)
        users = session.query(User).filter(User.id.in_(request.user_ids))
        for user in users:
            user.grant_point(request.amount)


@user_router.get(
    '',
    response_model=GetUsersResponse,
    description='학생 정보 전체 조회'
)
def get_users(auth: AuthJWT = Depends(), session=Depends(get_db)):
    check_is_admin(auth, session)
    users = [UserResponse.from_orm(user) for user in session.query(User).all()]
    return GetUsersResponse(users=users)
