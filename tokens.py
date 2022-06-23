from datetime import datetime, timedelta
from decouple import config
from jose import jwt


def create_access_token(data: dict, expires_delta):
    expire = datetime.utcnow() + expires_delta
    data.update({"exp": expire})  # by adding exp key jwt when decoding will check if token expired
    encoded_jwt = jwt.encode(data, config('SECRET_KEY'), algorithm=config('ALGORITHM'))
    return encoded_jwt



