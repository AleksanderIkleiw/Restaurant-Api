from pydantic import BaseModel, Field
from typing import Union


class Address(BaseModel):
    address: str
    address_line_2: Union[str, None] = None
    city: str
    postal_code: str
    phone_number: str


class User(BaseModel):
    username: str
    password: str


class Order(BaseModel):
    status: str
    firstname: str
    lastname: str
    address: Address
    user: User


class Menu(BaseModel):
    title: str
    description: str

