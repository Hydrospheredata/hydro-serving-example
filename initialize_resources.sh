#!/bin/bash

COMPOSE_FILE=$1
[ -z "$COMPOSE_FILE" ] && COMPOSE_FILE="docker-compose.yml"

docker-compose -f $COMPOSE_FILE exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic test
docker-compose -f $COMPOSE_FILE exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic success
docker-compose -f $COMPOSE_FILE exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic failure
docker-compose -f $COMPOSE_FILE exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic shadow_topic

GF_SECURITY_ADMIN_PASSWORD=$(grep GF_SECURITY_ADMIN_PASSWORD $COMPOSE_FILE | cut -d = -f 2 | cut -d '"' -f 1)

curl http://admin:${GF_SECURITY_ADMIN_PASSWORD}@localhost:3000/api/datasources -X POST -H 'Content-Type: application/json;charset=UTF-8' \
   --data-binary '{"Name":"Prometheus","Type":"prometheus","url":"http://prometheus:9090","Access":"proxy","isDefault":true}'

for i in $(ls grafana | grep json); do
   curl http://admin:${GF_SECURITY_ADMIN_PASSWORD}@localhost:3000/api/dashboards/db -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary "@./grafana/$i"
done