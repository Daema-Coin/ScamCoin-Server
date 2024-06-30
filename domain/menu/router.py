from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from database import session
from domain.menu.dto import CreateMenuRequest, GetMenusResponse, MenuResponse
from domain.menu.model import Menu
from domain.menu.service import get_booth_menu_by_id
from util import get_current_booth

menu_router = APIRouter(prefix="/menu")


@menu_router.post(
    '',
    status_code=201,
    description='메뉴 생성'
)
def create_menu(request: CreateMenuRequest, auth: AuthJWT = Depends()) -> None:
    booth = get_current_booth(auth)
    menu = Menu.of(request, booth.id)
    session.add(menu)
    session.commit()


@menu_router.put(
    '/{menu_id}',
    status_code=204,
    description='상품 판매 가능 여부 변경'
)
def update_sellable(menu_id: int, auth: AuthJWT = Depends()):
    booth = get_current_booth(auth)
    menu = session.query(Menu).filter_by(id=menu_id).one()
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    if menu.booth_id != booth.id:
        raise HTTPException(status_code=403, detail="Invalid Booth")

    menu.update_sellable()
    session.commit()


@menu_router.get(
    '',
    response_model=GetMenusResponse,
    description='내 부스 매뉴 조회'
)
def get_my_menu(auth: AuthJWT = Depends()):
    current_booth = get_current_booth(auth)
    return get_booth_menu_by_id(current_booth.id)


@menu_router.get(
    '/{booth_id}',
    response_model=GetMenusResponse,
    description='부스 매뉴 조회'
)
def get_booth_menu(booth_id: int):
    return get_booth_menu_by_id(booth_id)