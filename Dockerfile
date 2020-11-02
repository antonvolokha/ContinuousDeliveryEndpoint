FROM python:3.9.0-alpine3.12

RUN apk add build-base && pip --no-cache-dir install flask

WORKDIR /app/

COPY . /app/

CMD [ "python", "main.py" ]