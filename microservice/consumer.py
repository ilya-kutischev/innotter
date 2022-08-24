import json
import pika
import asyncio
import aio_pika
import logging
from aio_pika import connect, connect_robust
from user import (
    create_user,
    get_user,
    get_users,
    delete_user,
    update_user

)

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

    # @staticmethod
    # async def produce(message):
    #     routing_key = "core"
    #     connection = await connect('amqp://admin:admin@rabbitmq:5672')
    #
    #     async with connection:
    #         channel = await connection.channel(publisher_confirms=False)
    #
    #         async with channel.transaction():
    #             message = aio_pika.Message(body="There is message: {}".format(message).encode())
    #             await channel.default_exchange.publish(message, routing_key=routing_key, mandatory=False)

    async def process_incoming_message(self, message):
        await message.ack()
        # self.process_callable(message.body.decode('utf-8'))
        # message = json.loads(message)
        message = json.loads(message.body.decode('utf-8'))
        print("______________________________________________________")
        print(message)
        print(message["user"])
        user = get_user(message["user"])
        if user == []:
            print("CREATED EMPTY USER")
            user = {
              "id": message["user"],
              "posts": 0,
              "likes": 0,
              "followers": 0,
              "follow_requests": 0
            }
            create_user(user)

        print("NEW USER+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        user = user[0]
        print(user)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        if "posts" in list(message.keys()):
            user["posts"] += message["posts"]
        if "likes" in list(message.keys()):
            user["likes"] += message["likes"]
        if "followers" in list(message.keys()):
            user["followers"] += message["followers"]
        if "follow_requests" in list(message.keys()):
            user["follow_requests"] += message["follow_requests"]

        print("WHATS DONE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(user)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        update_user(user)
