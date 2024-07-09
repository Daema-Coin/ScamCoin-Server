from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Booth(Base):
    __tablename__ = "booth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_code = Column(String(10), nullable=False)
    name = Column(String(20), nullable=False)
    profit = Column(Integer, nullable=False)
    is_admin = Column(Boolean, nullable=False)

    def update_profit(self, price):
        self.profit += price
