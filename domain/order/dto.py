from pydantic import BaseModel


class OrderList(BaseModel):
    menu_id: int
    amount: int


class OrderRequest(BaseModel):
    orders: list[OrderList]
    request: str
    price: int
    booth_id: int


class Menu(BaseModel):
    menu: str
    amount: int
    price: int


class QueryOrder(BaseModel):
    order_id: int
    orderer_name: str
    request: str
    menu_list: list[Menu]


class QueryOrderLists(BaseModel):
    orders: list[QueryOrder]
