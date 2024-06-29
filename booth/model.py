from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Booth(Base):
    __tablename__ = "booth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    coin_balance = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
