from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Booth(Base):
    __tablename__ = "booth"
    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_code = Column(String(10), nullable=False)
    name = Column(String(20), nullable=False)
    profit = Column(Integer, nullable=False)
