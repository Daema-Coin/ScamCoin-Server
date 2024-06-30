import requests
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.user.dto import TokenResponse
from domain.user.model import User

XQUARE_API_SERVER = 'https://prod-server.xquare.app/dsm-login/user/user-data'


def _format_student_gcn(grade: int, class_num: int, student_num: int) -> str:
    student_num_str = f"{student_num:02}"
    student_id = f"{grade}{class_num}{student_num_str}"
    return student_id


def user_login(account_id: str, password: str, auth: AuthJWT):
    param = {
        'account_id': account_id,
        'password': password
    }

    result = requests.get(XQUARE_API_SERVER, params=param)
    if result.status_code == 401:
        raise HTTPException(status_code=401, detail='Invalid Password')
    if result.status_code == 404:
        raise HTTPException(status_code=404, detail='User not found')

    result = result.json()
    user = session.query(User).filter_by(account_id=account_id).first()
    gcn = _format_student_gcn(
        grade=result['grade'],
        class_num=result['class_num'],
        student_num=result['num']
    )
    if user is None:
        user = User(
            account_id=account_id,
            name=result['name'],
            gcn=gcn,
            coin_balance=0
        )
        session.add(user)
        session.commit()

    token = auth.create_access_token(
        subject=user.id,
        user_claims={
            'type': 'user'
        },
        algorithm='HS256',
        expires_time=60 * 60 * 24)
    return TokenResponse(
        token=token
    )
