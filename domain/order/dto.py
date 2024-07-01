from pydantic import BaseModel


class OrderList(BaseModel):
    menu_id: int
    amount: int


class OrderRequest(BaseModel):
    orders: list[OrderList]
    request: str
    price: int
