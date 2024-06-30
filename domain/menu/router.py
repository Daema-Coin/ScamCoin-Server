from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from starlette.status import HTTP_201_CREATED

from database import session
from domain.menu.dto import CreateMenuRequest
from domain.menu.model import Menu
from util import get_current_booth

menu_router = APIRouter(prefix="/menu")


@menu_router.post('', status_code=HTTP_201_CREATED)
def create_menu(request: CreateMenuRequest, auth: AuthJWT = Depends()) -> None:
    booth = get_current_booth(auth)
    menu = Menu.of(request, booth.id)
    session.add(menu)
    session.commit()
