# ==============================
FROM helsinkitest/python:3.7-slim as appbase
# ==============================
RUN mkdir /entrypoint

COPY --chown=appuser:appuser requirements.txt /app/requirements.txt

RUN apt-install.sh \
        git \
        netcat \
        libpq-dev \
        build-essential \
    && pip install -U pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-cleanup.sh build-essential

COPY --chown=appuser:appuser docker-entrypoint.sh /entrypoint/docker-entrypoint.sh
ENTRYPOINT ["/entrypoint/docker-entrypoint.sh"]

# ==============================
FROM appbase as development
# ==============================

COPY --chown=appuser:appuser requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r /app/requirements-dev.txt

ENV DEV_SERVER=1

COPY --chown=appuser:appuser . /app/

USER appuser
EXPOSE 8081/tcp

# ==============================
FROM appbase as production
# ==============================

COPY --chown=appuser:appuser . /app/

USER appuser
EXPOSE 8081/tcp
