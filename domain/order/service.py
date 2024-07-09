from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from database import transaction
from domain.order.dto import OrderRequest
from domain.order.model import Order, OrderLine
from util import get_current_user


def create_order(order_requests: OrderRequest, session: Session, authorize: AuthJWT):
    with transaction(session):
        user = get_current_user(authorize, session)
        order = Order(orderer_name=user.name,
                      request=order_requests.request,
                      status="request",
                      price=order_requests.price)
        session.add(order)
        session.commit()

        order_line = [
            OrderLine(order_id=order.id, menu_id=menu.menu_id, amount=menu.amount)
            for menu in order_requests.orders
        ]
        user.decrease_coin(order_requests.price)
        session.add_all(order_line)
