FROM frolvlad/alpine-python-machinelearning
LABEL artifactId=custom_scikit runtimeType=model version=1.0-SNAPSHOT

ENV RUNTIME_TYPE=model
ENV ENVOY_HTTP_PORT=8080 ENVOY_ADMIN_PORT=8082
ENV ZIPKIN_HOST=localhost ZIPKIN_PORT=9411 ZIPKIN_ENABLED=false
ENV MANAGER_HOST=localhost MANAGER_PORT=8080
ENV APP_HTTP_PORT=9090
ENV APP_START_SCRIPT=/app/start.sh
ENV ML_REPO_ADDR=localhost ML_REPO_PORT=8081
ENV MODEL_NAME=dummy MODEL_TYPE=custom_scikit MODEL_VERSION=1

ADD . /app/

WORKDIR /app
RUN apk update && \
    apk add --no-cache curl && \
    apk add gcc g++ linux-headers gfortran musl-dev python3-dev && \
    chmod +x /app/sidecar.sh && \
    chmod +x /app/start.sh && \
    ./sidecar.sh --target /hydro-serving/sidecar -- alpine && \
    rm -rf sidecar.sh && rm -rf /var/cache/apk/* && \
    ln -s locale.h /usr/include/xlocale.h

RUN pip install -r requirements.txt
RUN python3 nltk_prepare_env.py

WORKDIR /app/src

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://localhost:8080/health || exit 1
CMD ["/hydro-serving/sidecar/start.sh"]
