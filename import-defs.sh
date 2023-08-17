#!/bin/sh

set -e

for SVC in rmq0-hdc rmq0-odc
do
    # NB: https://github.com/docker/compose/issues/1262
    container_id="$(docker compose ps -q "$SVC")"
    docker exec "$container_id" /opt/rabbitmq/sbin/rabbitmqctl await_startup
    docker exec "$container_id" /opt/rabbitmq/sbin/rabbitmqctl import_definitions /etc/rabbitmq/definitions.json
done
