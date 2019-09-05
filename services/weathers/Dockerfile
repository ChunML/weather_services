FROM python:3.7.4-alpine

ENV http_proxy http://172.23.112.52:8080
ENV https_proxy https://172.23.112.52:8080
ENV ftp_proxy ftp://172.23.112.52:8080

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

WORKDIR /usr/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .

CMD ["./entrypoint.sh"]