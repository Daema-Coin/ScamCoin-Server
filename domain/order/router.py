from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from database import get_db, transaction
from domain.order.dto import OrderRequest
from domain.order.model import Order
from domain.order.service import create_order
from util import get_current_booth

order_router = APIRouter(prefix="/order")


@order_router.post("/", status_code=201, description="주문")
def order(request: OrderRequest, session=Depends(get_db), auth: AuthJWT = Depends()):
    create_order(request)


@order_router.put("/{order_id}", status_code=204, description='주문 상태 변경')
def update_order_status(status: str, order_id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    with transaction(session):
        get_current_booth(auth, session)
        order = session.query(Order).filter_by(id=order_id).first()
        order.update_order(status)
