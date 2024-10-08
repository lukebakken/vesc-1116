# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import argparse
import logging
import pika

log_fmt = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s"
log_date_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=log_fmt, datefmt=log_date_fmt)
logger = logging.getLogger()

parser = argparse.ArgumentParser(
    prog="consume.py", description="consume from inventory in hdc cluster"
)
parser.add_argument("-p", "--port", default="5672", type=int)
ns = parser.parse_args()
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
channel.basic_qos(prefetch_count=1)


def on_message(ch, method_frame, _header_frame, body):
    delivery_tag = method_frame.delivery_tag
    logger.info("consumed message: %d %s", delivery_tag, body)
    ch.basic_ack(delivery_tag)


channel.basic_consume(on_message_callback=on_message, queue="inventory")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
