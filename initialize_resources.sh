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


runtimeId=$(curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "name": "hydrosphere/serving-runtime-spark",
   "version": "2.1-latest",
   "modelTypes": [
     "spark:2.1"
   ],
   "tags": [
     "string"
   ],
   "configParams": {}
 }' 'http://localhost:80/api/v1/runtime' | jq '.id')

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "name": "hydrosphere/serving-runtime-spark",
   "version": "2.2-latest",
   "modelTypes": [
     "spark:2.2"
   ],
   "tags": [
     "string"
   ],
   "configParams": {}
 }' 'http://localhost:80/api/v1/runtime'

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
    "name": "hydrosphere/serving-runtime-spark",
    "version": "2.0-latest",
    "modelTypes": [
      "spark:2.0"
    ],
    "tags": [
      "string"
    ],
    "configParams": {}
  }' 'http://localhost:80/api/v1/runtime'


curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
    "name": "hydrosphere/serving-runtime-python",
    "version": "3.6-latest",
    "modelTypes": [
      "unknown:ssd_demo",
      "python:3.6"
    ],
    "tags": [
      "unknown:ssd_demo",
      "python:3.6"
    ],
    "configParams": {}
  }' 'http://localhost:80/api/v1/runtime'



modelId=$(curl -X GET --header 'Accept: application/json' 'http://localhost:80/api/v1/model' | jq -c '.[].model | select(.source | contains("local:word2vec"))| .id')

modelReleaseId=$(curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "modelId": '"$modelId"'
 }' 'http://localhost:80/api/v1/model/build' | jq '.id')

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "name": "test_application",
   "executionGraph": {
     "stages": [
       {
         "services": [
          {
            "runtimeId": '"$runtimeId"',
            "modelVersionId": '"$modelReleaseId"',
            "weight": 100,
            "signatureName": "default_spark"
          }
         ]
       }
     ]
   },
   "kafkaStreaming": [
     {
       "sourceTopic": "test",
       "destinationTopic": "success",
       "consumerId": "test_1",
       "errorTopic": "failure"
     }
   ]
 }' 'http://localhost:8080/api/v1/applications'
