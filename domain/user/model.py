from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    gcn = Column(String(4), nullable=False)
    account_id = Column(String(20), nullable=False)
    coin_balance = Column(Integer, nullable=False)

    def grant_point(self, coin):
        self.coin_balance += coin

    def decrease_coin(self, coin):
        if self.coin_balance < coin:
            raise HTTPException(status_code=403, detail="Not enough coins")
        self.coin_balance -= coin
