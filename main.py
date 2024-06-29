from fastapi import FastAPI

from booth.model import Booth
from database import Base, engine
from menu.model import Menu
from order.model import Order, OrderLine
from user.model import User

app = FastAPI()
Booth.metadata.create_all(bind=engine)
Menu.metadata.create_all(bind=engine)
Order.metadata.create_all(bind=engine)
OrderLine.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
