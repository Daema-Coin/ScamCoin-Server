from pydantic import BaseModel


class BoothLoginRequest(BaseModel):
    auth_code: str