from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.booth.dto import BoothLoginRequest, BoothLoginResponse
from domain.booth.model import Booth

booth_router = APIRouter(prefix="/booth")


@booth_router.post('/login')
def login(request: BoothLoginRequest, auth: AuthJWT = Depends()):
    booth = session.query(Booth).filter_by(auth_code=request.auth_code).first()
    if booth is None:
        raise HTTPException(status_code=401, detail="Invalid auth code")

    token = auth.create_access_token(subject=booth.id, algorithm='HS256', expires_time=60 * 60 * 24)
    return BoothLoginResponse(
        token=token,
        is_admin=booth.is_admin,
    )