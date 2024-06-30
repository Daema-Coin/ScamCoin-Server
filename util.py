from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.booth.model import Booth
from domain.user.model import User

invalid_user_exception = HTTPException(detail='Invalid User', status_code=401)
invalid_token_exception = HTTPException(detail='Invalid Token', status_code=401)


def _get_token_subject(auth: AuthJWT) -> str:
    auth.jwt_required()
    return auth.get_jwt_subject()


def _check_token_type(auth: AuthJWT, typ: str):
    if auth.get_raw_jwt()['auth'] != typ:
        raise invalid_token_exception


def get_current_user(authorize: AuthJWT):
    subject = _get_token_subject(authorize)
    _check_token_type(authorize, 'user')
    current_user = session.query(User).filter_by(id=subject).first()
    if current_user is None:
        raise invalid_user_exception

    return current_user


def get_current_booth(authorize: AuthJWT):
    subject = _get_token_subject(authorize)
    _check_token_type(authorize, 'booth')
    current_booth = session.query(Booth).filter_by(id=subject).first()
    if current_booth is None:
        raise invalid_user_exception

    return current_booth


def check_is_admin(auth: AuthJWT):
    booth = get_current_booth(auth)
    if not booth.is_admin:
        raise HTTPException(status_code=403, detail='Invalid Role')
