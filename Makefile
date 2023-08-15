.PHONY: clean down import up

RABBITMQ_DOCKER_TAG ?= 3.11.19-management

clean: down
	docker compose rm

down:
	docker compose down

import:
	/bin/sh $(CURDIR)/import-defs.sh

up:
	# NB: fresh stuffs
	# docker compose build --no-cache --pull --build-arg RABBITMQ_DOCKER_TAG=$(RABBITMQ_DOCKER_TAG)
	# docker compose up --pull always
	docker compose build --build-arg RABBITMQ_DOCKER_TAG=$(RABBITMQ_DOCKER_TAG)
	docker compose up
