from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from database import get_db, transaction
from domain.order.dto import OrderRequest
from domain.order.service import create_order

order_router = APIRouter(prefix="/order")


@order_router.post("/", status_code=201, description="주문")
def order(request: OrderRequest, session=Depends(get_db), auth: AuthJWT = Depends()):
    create_order(request)
