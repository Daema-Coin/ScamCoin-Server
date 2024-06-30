from database import session
from domain.menu.dto import MenuResponse, GetMenusResponse
from domain.menu.model import Menu


def get_booth_menu_by_id(booth_id: int, hide_sold_out: bool):
    query = session.query(Menu).filter_by(booth_id=booth_id)
    if hide_sold_out:
        query = query.filter_by(is_open=True)
    menus = query.all()
    result = [MenuResponse.from_orm(menu) for menu in menus]

    return GetMenusResponse(menu=result)
