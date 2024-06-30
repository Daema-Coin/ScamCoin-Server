from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base
from domain.menu.dto import CreateMenuRequest


class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    sell_count = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    image_url = Column(String(100), nullable=False)
    is_open = Column(Boolean, nullable=False)
    booth_id = Column(Integer, ForeignKey('booth.id'), nullable=False)

    @staticmethod
    def of(dto: CreateMenuRequest, booth_id: int):
        return Menu(
            name=dto.name,
            price=dto.price,
            description=dto.description,
            image_url=dto.image_url,
            sell_count=0,
            is_open=True,
            booth_id=booth_id
        )

    def update_sellable(self):
        self.is_open = not self.is_open
