FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src/ .

RUN mkdir /output

ENV ENV=""

CMD ["python", "./main.py"]