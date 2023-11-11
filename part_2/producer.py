from mongoengine import *
import pika
from faker import Faker
from models import Contact


fake = Faker()


def create_user(quantity):
    for _ in range(quantity):
        Contact(name=fake.name(),
                email=fake.email()).save()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='hw8_mock', exchange_type='direct')
channel.queue_declare(queue='hw8_queue', durable=True)
channel.queue_bind(exchange='hw8_mock', queue='hw8_queue')


def main():
    for user in Contact.objects():
        message = str(user.id)

        channel.basic_publish(
            exchange='hw8_mock',
            routing_key='hw8_queue',
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print('[x] Sent %r' % message)
    connection.close()


if __name__ == '__main__':
    if not Contact.objects():
        create_user(30)
    main()