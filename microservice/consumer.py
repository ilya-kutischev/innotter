import json
import pika
import asyncio
import aio_pika
import logging
from aio_pika import connect, connect_robust

logger = logging.getLogger(__name__)


class PikaClient:

    def __init__(self, process_callable):
        self.process_callable = process_callable

    async def consume(self, loop):
        connection = await connect_robust('amqp://admin:admin@rabbitmq:5672', loop=loop)

        channel = await connection.channel()
        queue = await channel.declare_queue('statistics')

        await queue.consume(self.process_incoming_message, no_ack=False)

        logging.info('Established pika async listener')
        return connection

    @staticmethod
    async def produce(message):
        routing_key = "core"
        connection = await connect('amqp://admin:admin@rabbitmq:5672')

        async with connection:
            channel = await connection.channel(publisher_confirms=False)

            async with channel.transaction():
                message = aio_pika.Message(body="There is message: {}".format(message).encode())
                await channel.default_exchange.publish(message, routing_key=routing_key)

    async def process_incoming_message(self, message):
        await message.ack()
        self.process_callable(message.body.decode('utf-8'))


































#def consume():
#     print("entred function")
#     # params = pika.URLParameters('amqp://admin:admin@localhost:5672/')
#     connection = pika.BlockingConnection(params)
#     channel = connection.channel()
#     channel.exchange_declare(exchange='Microservice', exchange_type='direct', durable=True)
#
#     result = channel.queue_declare(queue='statistics',exclusive=True, durable=True)
#     queue_name = result.method.queue
#     print("STARTED CONSUMER")
#
#
#     # RECIEVING MESSAGE AND ADDING TO DB
#     def callback(ch, method, properties, body):
#
#         print('Received message from admin')
#         data = json.loads(body)
#         print(data)
#
#
#         # if properties.content_type == 'product_created':
#         #     serializer = ProductSerializer(data=data)
#         #     if serializer.is_valid():
#         #         serializer.save()
#         #         print(f" Saved to database")
#         # else:
#         #     print(f" Not saved")
#
#     # channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)
#
#     try:
#         print("Starting consumer")
#         channel.start_consuming()
#     except KeyboardInterrupt:
#         channel.stop_consuming()
#         connection.close()
#         print("Stopping consumer")
# # this deletes the queue
# # channel.close()