FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get -y install curl git wget gpg gcc kmod\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# ultraleapのリポジトリを追加
RUN wget -qO - https://repo.ultraleap.com/keys/apt/gpg | gpg --dearmor | tee /etc/apt/trusted.gpg.d/ultraleap.gpg
RUN echo 'deb [arch=amd64] https://repo.ultraleap.com/apt stable main' | tee /etc/apt/sources.list.d/ultraleap.list
RUN apt update && yes | apt install ultraleap-hand-tracking

# poetryのインストール
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /workspace
VOLUME ["/workspace"]