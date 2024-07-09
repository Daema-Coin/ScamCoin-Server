from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from domain.order.dto import OrderList


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    orderer_name = Column(String(20), nullable=False)
    request = Column(String(100), nullable=False)
    status = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    order_lines = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")

    def update_order(self, status: str):
        self.status = status


class OrderLine(Base):
    __tablename__ = "order_line"
    order_id = Column(Integer, ForeignKey('order.id', ondelete="CASCADE"), primary_key=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), primary_key=True)
    amount = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_lines")
    menu = relationship("Menu", back_populates="order_lines")

    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'menu_id'),
    )
