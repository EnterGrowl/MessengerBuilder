FROM python:alpine3.7
RUN apk add --no-cache git
COPY . /app
WORKDIR /app
RUN python -m venv .
RUN source ./bin/activate
RUN pip install -r requirements.txt