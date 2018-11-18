import json
from threading import Thread, Timer

import pika

from utils import config
from utils import security


def init():
    t = Thread(target=listen_auth_logout, daemon=True)
    t.start()


def listen_auth_logout():
    exchange = 'auth'

    try:
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )

        chan = conn.channel()
        chan.exchange_declare(exchange=exchange, exchange_type='fanout')

        result = chan.queue_declare(exclusive=True)
        queue_name = result.method.queue

        chan.queue_bind(exchange=exchange, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.loads(body.decode())

            if event.get('type', 'None') == 'logout':
                security.invalidate_session(event.get('message'))

        chan.basic_consume(callback, queue=queue_name, no_ack=True)

        chan.start_consuming()

    except Exception as e:
        print(e)
        Timer(10.0, init).start()
