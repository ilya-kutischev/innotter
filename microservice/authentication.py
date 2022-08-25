import os
from fastapi import HTTPException
from dotenv import load_dotenv, find_dotenv
import jwt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innotter.settings')

load_dotenv(find_dotenv())
ALGORITHM =os.environ['ALGORITHM']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


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
