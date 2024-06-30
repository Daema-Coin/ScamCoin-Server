from pydantic import BaseModel


class CreateMenuRequest(BaseModel):
    name: str
    description: str
    price: int
    image_url: str