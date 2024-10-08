#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace

readonly cluster_name="${1:-hdc}"

for idx in 0 1 2
do
    service="rmq$idx-$cluster_name"

    echo "$(date +'%Y%m%dT-%H%M%S') [INFO] putting '$service' into maintenance mode..."
    docker compose exec "$service" rabbitmq-upgrade drain

    echo "$(date +'%Y%m%dT-%H%M%S') [INFO] restarting '$service'..."
    docker compose restart "$service"

    set +o errexit
    while ! docker compose exec "$service" rabbitmqctl await_startup
    do
        echo "$(date +'%Y%m%dT-%H%M%S') [INFO] waiting for '$service' to start..."
    done
    set -o errexit
done
