from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str


class RegisterUser(BaseModel):
    username: str
    password: str


class Address(BaseModel):
    address: str
    address_line_2: Union[str, None] = None
    city: str
    postal_code: str
    phone_number: str
    first_name: str
    surname: str


class Order(BaseModel):
    items: list[int]


class Menu(BaseModel):
    title: str
    description: str
    price: float
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
