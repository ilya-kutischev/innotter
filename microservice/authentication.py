import os
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"
# JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_SECRET_KEY = 'my_secret'
import jwt


async def get_current_user(token: str):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        print("PAYLOAD OF TOKEN : ", payload)

        user_id = payload['user_id']

        return user_id

    except:
        msg = 'Пользователь соответствующий данному токену не найден.'
        raise HTTPException(status_code=404, detail=msg)
