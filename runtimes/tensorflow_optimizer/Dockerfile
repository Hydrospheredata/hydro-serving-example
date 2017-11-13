FROM tensorflow/tensorflow:1.1.0-py3

ARG SIDECAR_VERSION=0.0.1

ENV SIDECAR_HTTP_PORT=8080
ENV APP_HTTP_PORT=9090
ENV APP_START_SCRIPT=/app/start.sh

ADD . /app/
ADD http://repo.hydrosphere.io/hydrosphere/static/hydro-serving-sidecar-install-$SIDECAR_VERSION.sh /app/sidecar.sh

WORKDIR /app

RUN apt update && \
    apt install -y curl && \
    chmod +x /app/sidecar.sh && sync && \
    chmod +x /app/start.sh && sync && \
    ./sidecar.sh --target /hydro-serving/sidecar -- ubuntu && \
    rm -rf sidecar.sh && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

WORKDIR /app/src

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:$APP_HTTP_PORT/health || exit 1
CMD ["/hydro-serving/sidecar/start.sh"]
