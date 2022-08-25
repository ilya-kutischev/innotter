from asyncio import sleep
from fastapi import FastAPI
from consumer import PikaClient
from db import create_tables
from routers import routes_user
import asyncio
import logging

logger = logging.getLogger('uvicorn.info')


class StatApp(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message):
        logger.info(f'{message}')


app = StatApp()

app.include_router(routes_user, prefix='')

create_tables()

@app.on_event('startup')
async def startup():
    await sleep(7)
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


# @app.get('/statistics')
# async def get_info_microservice():
#     logger.info('get_info_microservice method is called')
#     await app.pika_client.produce('')
#
#     return JSONResponse(content={'status': 'success'})



