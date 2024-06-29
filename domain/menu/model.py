from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


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