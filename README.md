# hydro-serving-runtime

#### Start demo environment
```
docker-compose up -d
```
#### Create topics
```
docker-compose exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic test
docker-compose exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic success
docker-compose exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic failure
docker-compose exec kafka kafka-topics --create --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181 --topic shadow_topic
```

#### Install hydro-serving cli
```
pip install hs
```

#### Add Spark Runtime
##### using hs-cli 
```
TBD

```

##### using curl + jq
```
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
 }' 'http://localhost:8080/api/v1/runtime' | jq '.id')

```

#### Release Model, Create Application
##### using hs-cli 
```
TBD

```

##### using curl + jq
```
#Find `word2vec`
modelId=$(curl -X GET --header 'Accept: application/json' 'http://localhost:8080/api/v1/model' | jq -c '.[].model | select(.name | contains("word2vec"))| .id')

#Release model
modelReleaseId=$(curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ 
   "modelId": '"$modelId"' 
 }' 'http://localhost:8080/api/v1/model/build' | jq '.id')
 
#Deploy application with new model version
applicationId=$(curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ 
   "name": "Test", 
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
 }' 'http://localhost:8080/api/v1/applications' | jq '.id')
```

##### using UI
TBD

#### Serve your application
##### using hs-cli 
TBD

##### using curl
```
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ 
   "text": "Some Test Text" 
 }' http://localhost:8080/api/v1/applications/serve/$applicationId/default_spark 
```
##### using UI
TBD

##### using python
TBD

##### using scala
TBD

## Other use full commands
#### Kafka commands
```
#create topic
docker-compose exec kafka kafka-topics --create --topic foodocker --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

#produce message from console
docker-compose exec kafka kafka-console-producer --topic foo --broker-list kafka:9092

#Consume all messages from kafka
docker-compose exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic foo --from-beginning
```

To connect to kafka from your HOST use `localhost:19092` as `broker.list`. Zookeeper on localhost:2181