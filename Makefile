.PHONY: clean down import up

RABBITMQ_DOCKER_TAG ?= 3-management

clean: down
	docker compose rm

down:
	docker compose down --volumes

import:
	/bin/sh $(CURDIR)/import-defs.sh

up:
ifdef DOCKER_FRESH
	docker compose build --no-cache --pull --build-arg RABBITMQ_DOCKER_TAG=$(RABBITMQ_DOCKER_TAG)
	docker compose up --pull always
else
	docker compose build --build-arg RABBITMQ_DOCKER_TAG=$(RABBITMQ_DOCKER_TAG)
	docker compose up
endif
