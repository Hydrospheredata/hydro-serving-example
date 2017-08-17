#!/bin/sh

VERSION=$1

[ -z "$1" ] && VERSION="0.0.1"

echo "Building dependencies and Docker images for demo..."

echo "Runtimes:"
cd runtimes

echo "Spark Local ML..."
cd localml-spark
./sbt/sbt assembly
docker build --build-arg VERSION=$VERSION --no-cache -t hydro-serving/runtime-sparklocal .
cd ../

echo "Scikit..."
cd scikit
docker build --build-arg VERSION=$VERSION -t mist-envoy-alpine-python-machinelearning -f Dockerfile-alpine-python-machinelearning .
docker build --build-arg VERSION=$VERSION --no-cache -t hydro-serving/runtime-scikit .
cd ../

echo "Custom Scikit..."
cd custom_scikit
docker build --build-arg VERSION=$VERSION --no-cache -t hydro-serving/runtime-customscikit .
cd ../

echo "Tensorflow..."
cd tensorflow
docker build --build-arg VERSION=$VERSION --no-cache -t hydro-serving/runtime-tensorflow -f Dockerfile-tensorflow-cpu .
cd ../

cd ../

echo "Build complete. Images are ready to run."
