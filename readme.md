## Angel


**on Desktop in ~/Weather**

build image
```bash
docker build -t angel:1.0 -f Dockerfile .
```

run image
```bash
docker run -d --net=host angel:1.0
```

build via docker-compose
```bash
docker-compose -f docker-compose.yml build
```

run via docker-compose
```bash
docker-compose -f docker-compose.yml up -d
```




**backup db**
```bash
MongoDB-3.6.1/bin/mongodump --db=language --collection=english --out=/home/jd/Dropbox/backup/angel-13-01-2017
```

**restore db**
```bash
MongoDB-3.6.1/bin/mongorestore --db=language --collection=english /home/jd/Dropbox/backup/angel-13-01-2017/language/english.bson
```




$ docker pull mongo:3.6.1-jessie

start a mongo instance
$ docker run --name angel-mongo -v /home/jd/data/db:/data/db -d mongo

connect to it from an application
$ docker run --name angel-app --link angel-mongo:mongo -d angel:1.0

... or via mongo
$ docker run -it --link angel-mongo:mongo --rm mongo sh -c 'exec mongo "$MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT/test"'


https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


https://download.docker.com/linux/ubuntu/dists/xenial/pool/stable/amd64/docker-ce_17.12.0~ce-0~ubuntu_amd64.deb

sudo dpkg -i docker-ce_17.12.0~ce-0~ubuntu_amd64.deb


sudo groupadd docker
sudo gpasswd -a $USER docker
