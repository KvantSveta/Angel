FROM python:3.6.4-stretch

ADD . /home

WORKDIR /home

RUN apt-get update \
 && pip install -U -r requirements.txt \
 && apt-get clean

RUN echo "Europe/Moscow" > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.6", "main/web.py"]
