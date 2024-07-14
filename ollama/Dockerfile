# Ubuntu minimalをベースイメージとして使用
FROM ubuntu:22.04

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Ollamaをインストール
RUN curl -fsSL https://ollama.com/install.sh | sh

# Ollamaのデータディレクトリを作成
RUN mkdir -p /root/.ollama

COPY run.sh /root/run.sh

ENV OLLAMA_HOST 0.0.0.0
ENV MODEL_NAME=""

# ポート11434を公開
EXPOSE 11434

# Ollamaを実行
CMD ["sh", "/root/run.sh"]
