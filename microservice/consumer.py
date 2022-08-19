import json
import pika
import django
import time

params = pika.URLParameters('amqp://test:test@localhost:5672/')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='Microservice', exchange_type='direct', durable=True)

channel.queue_declare(queue='statistics', durable=True)
print("STARTED CONSUMER")
# RECIEVING MESSAGE AND ADDING TO DB
def callback(ch, method, properties, body):
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    print('Received message from admin')
    data = json.loads(body)
    print(data)

    # if properties.content_type == 'product_created':
    #     serializer = ProductSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(f" Saved to database")
    # else:
    #     print(f" Not saved")


channel.basic_consume(on_message_callback=callback, queue='statistics', auto_ack=True)

try:
    print("Starting consumer")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()
    print("Stopping consumer")

# this deletes the queue
# channel.close()