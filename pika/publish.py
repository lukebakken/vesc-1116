# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import argparse
import datetime
import logging
import pika

log_fmt = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s"
log_date_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=log_fmt, datefmt=log_date_fmt)
logger = logging.getLogger()

parser = argparse.ArgumentParser(
    prog="consume.py", description="consume from inventory-fed"
)
parser.add_argument("-i", "--interval", default="1", type=int)
parser.add_argument("-c", "--msgcount", default="100000", type=int)
parser.add_argument("-p", "--port", default="5672", type=int)
ns = parser.parse_args()
pub_interval = ns.interval
msg_count = ns.msgcount
rmq_port = ns.port

credentials = pika.PlainCredentials("guest", "guest")
parameters = pika.ConnectionParameters(
    host="localhost",
    port=rmq_port,
    virtual_host="/",
    credentials=credentials,
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
        if pub_interval > 0 or c % 5000 == 0:
            logger.info("publishing message %d: %s", c, b)
        channel.basic_publish(exchange="inventory", routing_key="/", body=b)
        connection.process_data_events(time_limit=pub_interval)
        if c >= msg_count:
            logger.info("done publishing! %d", c)
            break
        c += 1
    except KeyboardInterrupt:
        break

connection.close()
