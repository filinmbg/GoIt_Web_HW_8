import sys
import pika
from models import Contact


def send_message(id_):
    user = Contact.objects.get(id=id_)
    user.send_email = True
    user.save()
    fullname = user.name
    print(f'{fullname}, hello!')


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hw8_queue', durable=True)
    print('Waiting for messages')

    def callback(ch, method, properties, body):
        message = body.decode('UTF-8')
        send_message(message)
        print(f'[x] Done: {method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hw8_queue', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as error:
        print(f'{error}')
        sys.exit(0)