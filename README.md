# Restaurant API

The project provides API for login/register, creating orders and many more.



## Deployment

To deploy this project, run

```bash
 npm run deploy
```


## Deployment

To deploy this project, create a .env file and set variables

`HOST_NAME=localhost` Database host name \
`DATABASE_NAME=restaurant` self explainatory \
`USER_NAME=admin` database's user \
`PASSWORD=admin` database's password \
`PORT=5432` port on which database is running \
`USER_DATABASE_NAME=restaurant_user` name of the user table \
`ADDRESS_DATABASE_NAME=address` name of the address table \
`ORDER_DATABASE_NAME=restaurant_order` name of the order table \
`MENU_DATABASE_NAME=menu` name of the menu table \
`SECRET_KEY` JWT secret key that you need to generate \
`ALGORITHM=HS256` algorithm of hashing \
`ACCESS_TOKEN_EXPIRE_SECONDS` seconds after which token expires \
`ACCESS_TOKEN_EXPIRE_MINUTES=30` minutes after which token expires \
`ACCESS_TOKEN_EXPIRE_HOURS` hours after which token expires \
`ACCESS_TOKEN_EXPIRE_DAYS` days after which token expires


## Installation

To run the project you need to install docker, get adminer and postgresql images and  run those commands

```bash
 git clone https://github.com/AleksanderIkleiw/Restaurant-Ap
 cd bookstore
 pip install -r requirements.txt
 docker-compose up -d
 python main.py
```
When you run the project for the first time, you also need to create the necessary tables in the database. It can be done by running the following command
```bash
python database.py
```  

## API Reference
You can access all methods http://127.0.0.1:8000/docs
#### Get all items from the menu

```http
GET /menu
```

| Authorization |              
| :-------- |
| Required |


#### Set your address

```http
PUT /set_address
```

| Parameter | Type     | Required/Not Required                       |
| :-------- | :------- | :-------------------------------- |
| `address`| `string` | **Required**|
| `address_line_2`      | `string` | **Not Required**|
| `city`      | `string` | **Required**|
| `postal_code`      | `string` | **Required**.|
| `phone_number`      | `string` | **Required**|
| `first_name`      | `string` | **Required**|
| `surname`      | `string` | **Required**|



## Features

- Saving orders to the database with a unique id
- authorization via OAUTH2
- Possibility of implementing additional services like email verification/order status change
