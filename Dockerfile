ARG JINA_VERSION=3.14.1

FROM jinaai/jina:${JINA_VERSION}-py38-standard

RUN pip install fastapi==0.95.1 uvicorn==0.22.0 starlette==0.26.1

COPY . /workspace/
WORKDIR /workspace

ENTRYPOINT ["jina", "executor", "--uses", "config.yml", "--timeout-ready", "3600000"]