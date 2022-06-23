from enum import Enum
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User, Token, Menu, Order, Address, RegisterUser
import database
from hashing import hash_password, generate_random_hash
from tokens import create_access_token
from datetime import timedelta
from jose import jwt, JWTError
from decouple import config

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Constants(Enum):
    secret_key = config('SECRET_KEY')
    algorithm = config('ALGORITHM')
    access_token_lifetime_seconds = config('ACCESS_TOKEN_EXPIRE_SECONDS', default=0, cast=int)
    access_token_lifetime_minutes = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=0, cast=int)
    access_token_lifetime_hours = config('ACCESS_TOKEN_EXPIRE_HOURS', default=0, cast=int)
    access_token_lifetime_days = config('ACCESS_TOKEN_EXPIRE_DAYS', default=0, cast=int)


async def validate_token_return_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        """
        tries to decode bearer header
        """
        payload = jwt.decode(token,
                             Constants.secret_key.value,
                             algorithms=[Constants.algorithm.value])
        username = payload.get("username")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    """
    checks if username is in the database, and if it is,
    converts memory object retrieved from the database to bytes
    """

    return User(username=username)


@app.post('/token/', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = RegisterUser(username=form_data.username, password=form_data.password).dict()
    user.update({'password': hash_password(user['password'])})  # hashes user provided password
    if database.login(user):  # if user exists and provided proper password, creates token
        access_token = create_access_token(
            data={"username": user['username']},
            expires_delta=timedelta(seconds=Constants.access_token_lifetime_seconds.value,
                                    minutes=Constants.access_token_lifetime_minutes.value,
                                    hours=Constants.access_token_lifetime_hours.value,
                                    days=Constants.access_token_lifetime_days.value)
        )
        return {'access_token': access_token, 'token_type': 'bearer'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},
                        )


@app.post('/register/')
async def register(form_data: RegisterUser):
    print(form_data)
    user = form_data.dict()
    user.update({'password': hash_password(user['password'])})

    return database.register(user)


@app.get('/menu')
async def menu(user: User = Depends(validate_token_return_user)):
    if not (menu_dicts := database.get_menu()):
        return 'Menu is empty.'
    menu_dicts = [Menu(title=menu_object[0],
                       description=menu_object[1],
                       price=menu_object[2],
                       id=menu_object[3]).dict() for menu_object in menu_dicts]
    return menu_dicts


@app.post('/create-order')
async def create_order(form_data: Order, user: User = Depends(validate_token_return_user)):
    form_data = form_data.dict()
    address = database.get_user_address(user.username)

    if not address:
        return "Please set your account's address."

    items = database.check_if_item_id_in_table(form_data['items'])

    if len(items) != len(form_data['items']):
        return "One or more selected items doesn't exist"

    form_data.update({'status': 'Waiting for confirmation'})
    form_data.update({'order_id': (order_id := generate_random_hash())})
    form_data.update({'username': user.username})
    print(form_data)
    database.inset_into_order_table(form_data)
    return {'message': 'Order has been placed.', 'order_id': order_id}


@app.put('/set_address')
async def set_user_address(form_data: Address, user: User = Depends(validate_token_return_user)):
    form_data = form_data.dict()
    form_data.update({'username': user.username})
    database.insert_replace_address(form_data)
    return 'ok'


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
