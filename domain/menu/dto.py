from pydantic import BaseModel


class CreateMenuRequest(BaseModel):
    name: str
    description: str
    price: int
    image_url: str


class MenuResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    image_url: str
    sell_count: int
    is_open: bool

    class Config:
        orm_mode = True


class GetMenusResponse(BaseModel):
    booth_name: str
    menu: list[MenuResponse]
