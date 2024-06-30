from database import session
from domain.menu.dto import MenuResponse, GetMenusResponse
from domain.menu.model import Menu


def get_booth_menu_by_id(booth_id: int):
    menus = session.query(Menu).filter_by(booth_id=booth_id).all()
    result = [MenuResponse.from_orm(menu) for menu in menus]

    return GetMenusResponse(menu=result)
