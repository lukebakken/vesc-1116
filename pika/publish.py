# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import argparse
import datetime
import logging
import pika

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

parser = argparse.ArgumentParser(prog='consume.py', description='consume from inventory-fed')
parser.add_argument('-p', '--port', default='5672', type=int)
ns = parser.parse_args()
rmq_port = ns.port

credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(
    host="localhost", port=rmq_port, virtual_host="is-inventory", credentials=credentials
)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

msgprops = pika.BasicProperties(
    content_type="text/plain", delivery_mode=pika.DeliveryMode.Persistent
)

c = 0
while True:
    try:
        d = datetime.datetime.now()
        b = d.isoformat()
        if c % 1000 == 0:
            logger.info("publishing message %d: %s", c, b)
        channel.basic_publish(exchange="inventory", routing_key="is-inventory", body=b)
        connection.process_data_events()
        c += 1
    except KeyboardInterrupt:
        break

connection.close()
