#!/bin/sh

SERVICE_ID=$1

echo "Starting $SERVER_JAR"

exec java -jar $SERVER_JAR
