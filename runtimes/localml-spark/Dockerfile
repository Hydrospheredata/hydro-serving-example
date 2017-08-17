ARG VERSION=latest
FROM anapsix/alpine-java:8

ARG VERSION

ENV SIDECAR_HTTP_PORT=8080
ENV APP_HTTP_PORT=9090
ENV APP_START_SCRIPT=/app/start.sh

ENV SERVER_HOME=/app
ENV SERVER_JAR=spark-localml-serve-assembly-1.0.jar

ADD start.sh /app/
ADD http://repo.hydrosphere.io/hydrosphere/static/hydro-serving-sidecar-install-$VERSION.sh /app/sidecar.sh
ADD target/scala-2.11/${SERVER_JAR} /app/${SERVER_JAR}

WORKDIR /app

RUN apk update && \
    apk add --no-cache curl && \
    chmod +x /app/start.sh; sync; \
    && ./sidecar.sh --target /hydro-serving/sidecar -- alpine && \
    rm -rf sidecar.sh && rm -rf /var/cache/apk/*

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:8080/health || exit 1
CMD ["/hydro-serving/sidecar/start.sh"]
