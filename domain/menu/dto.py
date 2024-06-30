from pydantic import BaseModel


class CreateMenuRequest(BaseModel):
    name: str
    description: str
    price: int
    image_url: str


class MenuResponse(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    sell_count: int
    is_open: bool

    class Config:
        orm_mode = True


class GetMenusResponse(BaseModel):
    menu: list[MenuResponse]
