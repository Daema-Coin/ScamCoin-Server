from fastapi import APIRouter

user_router = APIRouter(prefix="/user")


@user_router.post('/login')
def user_login(type: str):
    if type == 'USER':
