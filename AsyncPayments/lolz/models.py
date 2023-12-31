from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    balance: float
    hold: float

class Payments(BaseModel):
    payments: dict
    page: int
    hasNextPage: bool
