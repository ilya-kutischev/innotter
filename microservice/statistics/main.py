from fastapi import FastAPI
from .db import create_tables, ddb
from .routers import routes_user

app = FastAPI()

app.include_router(routes_user, prefix='')

create_tables()
