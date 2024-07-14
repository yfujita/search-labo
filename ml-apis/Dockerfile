FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app/ .

ENV HF_ACCESS_TOKEN=""

CMD ["python", "./main.py"]