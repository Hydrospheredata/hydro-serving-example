#!/bin/sh

VERSION=$1
SIDECAR_VERSION=$2

[ -z "$1" ] && VERSION="0.0.1"
[ -z "$2" ] && SIDECAR_VERSION="0.0.1"

sbt -DsparkVersion=2.0.2 assembly
sbt -DsparkVersion=2.1.2 assembly
sbt -DsparkVersion=2.2.0 assembly

docker build --build-arg SPARK_VERSION=2.0 --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-sparklocal-2.0:$VERSION .
docker build --build-arg SPARK_VERSION=2.1 --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-sparklocal-2.1:$VERSION .
docker build --build-arg SPARK_VERSION=2.2 --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-sparklocal-2.2:$VERSION .

docker build --build-arg SPARK_VERSION=2.0 --build-arg VERSION=0.0.1 --build-arg SIDECAR_VERSION=0.0.1 --no-cache -t hydrosphere/serving-runtime-sparklocal-2.0:0.0.1 .
