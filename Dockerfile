FROM python:3.7.2-alpine3.9

COPY . /home

WORKDIR /home

RUN pip install -U -r requirements.txt

RUN apk update \
 && apk add tzdata \
 && cp -r -f /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.7", "main/web.py"]
