ARG VERSION=latest
FROM frolvlad/alpine-python-machinelearning

ARG VERSION

ENV SIDECAR_HTTP_PORT=8080
ENV APP_HTTP_PORT=9090
ENV APP_START_SCRIPT=/app/start.sh

ADD . /app/
ADD http://repo.hydrosphere.io/hydrosphere/static/hydro-serving-sidecar-install-$VERSION.sh /app/sidecar.sh

WORKDIR /app

RUN apk update && \
    apk add --no-cache curl && \
    apk add gcc g++ linux-headers gfortran musl-dev python3-dev && \
    chmod +x /app/sidecar.sh; sync; && \
    chmod +x /app/start.sh; sync; && \
    ./sidecar.sh --target /hydro-serving/sidecar -- alpine && \
    rm -rf sidecar.sh && rm -rf /var/cache/apk/* && \
    ln -s locale.h /usr/include/xlocale.h

RUN pip install -r requirements.txt

WORKDIR /app/src

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:8080/health || exit 1
CMD ["/hydro-serving/sidecar/start.sh"]
