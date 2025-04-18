FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get -y install curl git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /workspace
VOLUME ["/workspace"]