from pydantic import BaseModel, Field
from typing import Union


class User(BaseModel):
    username: str
    password: str


class Address(BaseModel):
    address: str
    address_line_2: Union[str, None] = None
    city: str
    postal_code: str
    phone_number: str
    user: User


class Order(BaseModel):
    status: str
    firstname: str
    lastname: str
    address: Address
    user: User


class Menu(BaseModel):
    title: str
    description: str


class Token(BaseModel):
    access_token: str
    token_type: str

