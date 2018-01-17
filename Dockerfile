FROM python:3.6.4-alpine3.7

ADD . /home

WORKDIR /home

RUN pip install -U -r requirements.txt

RUN apk update \
 && apk add tzdata \
 && cp -r -f /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.6", "main/web.py"]
