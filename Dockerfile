FROM python:3.11.0

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install --yes --no-install-recommends vim git

RUN  apt-get autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/src/llm_api

WORKDIR /app

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:${PATH}"

RUN pip install --no-cache-dir -U pip

COPY ./pyproject.toml /app
COPY ./src/llm_api /app/src/llm_api

RUN pip install .

ENTRYPOINT ["gunicorn", \
            "--config=python:llm_api.gunicorn_conf",  \
            "llm_api.main:app"]
