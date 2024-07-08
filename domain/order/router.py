import asyncio

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.orm import Session, join, joinedload
from sse_starlette import EventSourceResponse

from database import get_db, transaction
from domain.booth.model import Booth
from domain.menu.model import Menu
from domain.order.dto import OrderRequest, QueryOrderLists, QueryOrder
from domain.order.model import Order, OrderLine
from domain.order.service import create_order
from util import get_current_booth

order_router = APIRouter(prefix="/order")

event_queue = asyncio.Queue()


@order_router.post("/", status_code=201, description="주문")
async def order(request: OrderRequest, session=Depends(get_db), auth: AuthJWT = Depends()):
    create_order(request)
    await event_queue.put(request.dict())


@order_router.put("/{order_id}", status_code=204, description='주문 상태 변경')  # status = request/done
def update_order_status(status: str, order_id: int, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    with transaction(session):
        get_current_booth(auth, session)
        order = session.query(Order).filter_by(id=order_id).first()
        order.update_order(status)


async def event_generator():
    while True:
        data = await event_queue.get()
        yield {
            "order": data
        }


@order_router.get("/")
async def query_order_sse():
    return EventSourceResponse(event_generator())


@order_router.get("/lists", response_model=QueryOrderLists, description='주문 내역 조회')  # status = request/done
def query_order_lists(status: str, auth: AuthJWT = Depends(), session: Session = Depends(get_db)):
    booth = get_current_booth(auth, session)
    orders = (session.query(Order.id, Order.orderer_name, Order.request, Order.status, Menu.name, OrderLine.amount,
                            Menu.price)
              .select_from(Menu)
              .join(OrderLine, Menu.id == OrderLine.menu_id)
              .join(Order, OrderLine.order_id == Order.id)
              .filter(Menu.booth_id == booth.id)
              .filter(Order.status == status)
              .order_by(Order.id.desc())
              .all())

    order_dict = {}
    for order_id, orderer_name, request, status, menu_name, amount, menu_price in orders:
        if order_id not in order_dict:
            order_dict[order_id] = {
                "order_id": order_id,
                "orderer_name": orderer_name,
                "request": request,
                "menu_list": []
            }
        order_dict[order_id]["menu_list"].append({
            "menu": menu_name,
            "amount": amount,
            "price": menu_price
        })

    result_orders = [QueryOrder(**order) for order in order_dict.values()]
    return QueryOrderLists(orders=result_orders)
