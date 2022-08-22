import json
import pika
import asyncio
import aio_pika


async def consume(loop):
    print("entred function------------------------------------------")
    connection = await aio_pika.connect_robust('amqp://admin:admin@rabbitmq:5672/',loop=loop)
    queue_name = "statistics"
    routing_key = "statistics"
    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        print("222222222222222222222222222222222222")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                print(message)



































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