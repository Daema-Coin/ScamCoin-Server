from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from database import Base


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    orderer_name = Column(String(20), nullable=False)
    request = Column(String(100), nullable=False)
    status = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)


class OrderLine(Base):
    __tablename__ = "order_line"
    order_id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'menu_id'),
    )
