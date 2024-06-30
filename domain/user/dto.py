from pydantic import BaseModel


class GetUserCoinResponse(BaseModel):
    coin: int