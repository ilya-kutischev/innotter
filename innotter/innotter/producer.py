# import pika
import asyncio
import logging
import json
from asyncio import sleep

import aio_pika
from aio_pika import connect_robust, connect
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

#
# def publish(method='', exchange='', queue='statistics', message='Hello World!'):
#     #before start should create such user in rabbit
#     params = pika.URLParameters('amqp://test:test@rabbitmq:5672/')
#
#     connection = pika.BlockingConnection(params)
#     channel = connection.channel()
#
#     channel.basic_qos(prefetch_count=1)
#
#     channel.queue_declare(queue=queue, durable=True)
#     properties = pika.BasicProperties(method)
#
#     channel.basic_publish(exchange=exchange, routing_key=queue, body=json.dumps(message), properties=properties)
#     print(f" [admin producer] Sent a message: \n `{message}`")



class PikaClient:

    def __init__(self, process_callable):
        self.process_callable = process_callable

    async def consume(self, loop):
        connection = await connect_robust('amqp://admin:admin@rabbitmq:5672', loop=loop)

        channel = await connection.channel()
        queue = await channel.declare_queue('core')

        await queue.consume(self.process_incoming_message, no_ack=False)

        logging.info('Established pika async listener')
        return connection

    @staticmethod
    async def produce(message):
        routing_key = "statistics"
        connection = await connect('amqp://admin:admin@rabbitmq:5672')

        async with connection:
            channel = await connection.channel(publisher_confirms=False)

            async with channel.transaction():
                message = aio_pika.Message(body="There is message: {}".format(message).encode())
                await channel.default_exchange.publish(message, routing_key=routing_key)

    async def process_incoming_message(self, message):
        await message.ack()
        self.process_callable(message.body.decode('utf-8'))


def log_incoming_message(cls, message):
    logger.info(f'Incoming message in Core app: {message}')





async def wait_response():
    pika_client = PikaClient(log_incoming_message)
    loop = asyncio.get_running_loop()
    task = loop.create_task(pika_client.consume(loop))
    await task


async def publish():
    logger.info('PUBLISH method is called')
    pika_client = PikaClient(log_incoming_message)
    await pika_client.produce('Message from Core app')
    return JSONResponse(content={'status': 'success'})




