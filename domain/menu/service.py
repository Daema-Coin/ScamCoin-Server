from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.booth.model import Booth
from domain.menu.dto import MenuResponse, GetMenusResponse
from domain.menu.model import Menu


def get_booth_menu_by_id(booth_id: int, hide_sold_out: bool, session: Session):
    booth = session.query(Booth).filter_by(id=booth_id).one_or_none()
    query = session.query(Menu).filter_by(booth_id=booth_id)
    if hide_sold_out:
        query = query.filter_by(is_open=True)
    menus = query.all()
    result = [MenuResponse.from_orm(menu) for menu in menus]

    return GetMenusResponse(
        booth_name=booth.name,
        menu=result
    )


def get_menu_with_validation(menu_id: int, booth_id: int, session: Session):
    menu = session.query(Menu).filter_by(id=menu_id).one()
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    if menu.booth_id != booth_id:
        raise HTTPException(status_code=403, detail="Invalid Booth")

    return menu
