#!/bin/sh

VERSION=$1

SIDECAR_VERSION=$2

[ -z "$1" ] && VERSION="0.0.1"
[ -z "$2" ] && SIDECAR_VERSION="0.0.1"

echo "Building dependencies and Docker images for demo..."

echo "Runtimes:"
cd runtimes

echo "Spark Local ML..."
cd localml-spark
sh build.sh $VERSION $SIDECAR_VERSION
cd ../

echo "Scikit..."
cd scikit
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-scikit:$VERSION .
cd ../

echo "Databricks Python 2..."
cd databricks_python2
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-py2databricks:$VERSION .
cd ../

echo "Python3..."
cd function_py
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-python3:$VERSION .
cd ../

echo "Custom Scikit..."
cd custom_scikit
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-customscikit:$VERSION .
cd ../

echo "Tensorflow..."
cd tensorflow
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-tensorflow:$VERSION -f Dockerfile-tensorflow-cpu .
cd ../

echo "Tensorflow Optimizer..."
cd tensorflow_optimizer
docker build --build-arg VERSION=$VERSION --build-arg SIDECAR_VERSION=$SIDECAR_VERSION --no-cache -t hydrosphere/serving-runtime-tensorflow-optimizer:$VERSION .
cd ../

cd ../

echo "Build complete. Images are ready to run."
