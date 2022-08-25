# import pika
# import json
#
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
