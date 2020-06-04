FROM python:alpine3.7
RUN apk add --no-cache git
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN source ./bin/activate