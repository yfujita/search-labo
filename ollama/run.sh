#!/bin/bash
set -e

echo "Serve"
ollama serve &
OLLAMA_PID=$!

# サービスが起動するのを待つ
echo "Waiting for Ollama service to start..."
until curl -s -f -o /dev/null "http://localhost:11434/api/version"
do
  echo "Waiting for Ollama to be ready..."
  sleep 2
done

echo "Install Model ${MODEL_NAME}"
ollama pull $MODEL_NAME

tail --pid=$OLLAMA_PID -f /dev/null
