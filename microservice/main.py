from fastapi import FastAPI

from consumer import consume
from db import create_tables, ddb
from routers import routes_user
import asyncio
import logging
import uvicorn as uvicorn
from starlette.responses import JSONResponse

# app = FastAPI()

logger = logging.getLogger('uvicorn.info')


class StatApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consume = consume


app = StatApp()

app.include_router(routes_user, prefix='')


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.consume(loop))
    await task


create_tables()
