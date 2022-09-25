import logging
import aio_pika
from aio_pika import connect_robust, connect
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


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
                message = aio_pika.Message(body="{}".format(message).encode())
                await channel.default_exchange.publish(message, routing_key=routing_key)

    async def process_incoming_message(self, message):
        await message.ack()
        print(f"WE ARE IN PROCESSING MESSAGE FUNC, MESSAGE = {message}")
        self.process_callable(message.body.decode('utf-8'))


def log_incoming_message(cls, message):
    logger.info(f'{message}')


async def publish(message):
    logger.info('PUBLISH method is called')
    pika_client = PikaClient(log_incoming_message)
    await pika_client.produce(message)
    return JSONResponse(content={'status': 'success'})
