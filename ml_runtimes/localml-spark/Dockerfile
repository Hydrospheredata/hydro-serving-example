FROM anapsix/alpine-java:8

LABEL artifactId=spark runtimeType=model version=1.0-SNAPSHOT

ENV RUNTIME_TYPE=model
ENV ENVOY_HTTP_PORT=8080 ENVOY_ADMIN_PORT=8082
ENV ZIPKIN_HOST=localhost ZIPKIN_PORT=9411 ZIPKIN_ENABLED=false
ENV MANAGER_HOST=localhost MANAGER_PORT=8080
ENV APP_HTTP_PORT=9090
ENV APP_START_SCRIPT=/app/start.sh
ENV ML_REPO_ADDR=localhost ML_REPO_PORT=8081
ENV MODEL_NAME=dummy MODEL_TYPE=custom_scikit MODEL_VERSION=1

ENV SERVER_HOME=/app
ENV SERVER_JAR=spark-localml-serve-assembly-1.0.jar

ADD start.sh /app/
ADD sidecar.sh /app/
ADD target/scala-2.11/${SERVER_JAR} /app/${SERVER_JAR}

WORKDIR /app

RUN apk update && \
    apk add --no-cache curl && \
    chmod +x /app/start.sh && \
    ./sidecar.sh --target /hydro-serving/sidecar -- alpine && \
    rm -rf sidecar.sh && rm -rf /var/cache/apk/*

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:8080/health || exit 1
CMD ["/hydro-serving/sidecar/start.sh"]
