from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.booth.dto import BoothLoginRequest, BoothLoginResponse, GetBoothInfoResponse
from domain.booth.model import Booth
from util import get_current_booth

booth_router = APIRouter(prefix="/booth")


@booth_router.post(
    '/login',
    status_code=201,
    response_model=BoothLoginResponse,
    description='부스 로그인'
)
def login(request: BoothLoginRequest, auth: AuthJWT = Depends()):
    booth = session.query(Booth).filter_by(auth_code=request.auth_code).first()
    if booth is None:
        raise HTTPException(status_code=401, detail="Invalid auth code")

    token = auth.create_access_token(
        subject=booth.id,
        user_claims={
            'auth': 'booth'
        },
        algorithm='HS256',
        expires_time=60 * 60 * 24
    )
    return BoothLoginResponse(
        token=token,
        is_admin=booth.is_admin,
    )


@booth_router.get(
    '',
    response_model=GetBoothInfoResponse,
    description='내 부스 정보 조회'
)
def get_booth_info(auth: AuthJWT = Depends()):
    current_booth = get_current_booth(auth)
    return GetBoothInfoResponse.from_orm(current_booth)