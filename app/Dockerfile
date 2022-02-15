FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY test2.py .
ENTRYPOINT [ "python", "test2.py" ]