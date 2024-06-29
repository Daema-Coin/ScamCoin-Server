from fastapi import FastAPI
from fastapi.requests import Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from domain.booth.model import Booth
from domain.booth.router import booth_router
from database import engine
from domain.menu.model import Menu
from domain.menu.router import menu_router
from domain.order.model import Order, OrderLine
from domain.order.router import order_router
from domain.user.model import User
from domain.user.router import user_router

app = FastAPI()
Booth.metadata.create_all(bind=engine)
Menu.metadata.create_all(bind=engine)
Order.metadata.create_all(bind=engine)
OrderLine.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)


class Settings(BaseModel):
    authjwt_secret_key: str = "67e4f877235b093f4f3b9e6c5618451c48d97fb1b498f0c6"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(booth_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(user_router)
