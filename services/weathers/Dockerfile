FROM python:3.7.4-slim

# ENV http_proxy http://172.23.112.52:8080
# ENV https_proxy https://172.23.112.52:8080
# ENV ftp_proxy ftp://172.23.112.52:8080

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /usr/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

COPY . .

CMD ["./entrypoint.sh"]
