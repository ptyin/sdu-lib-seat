# docker run -d -p 8000:8000 ptyin/crontab-ui
FROM alpine:3.13.5

ENV CRON_PATH=/etc/crontabs
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

RUN   mkdir -p /crontab-ui/sdu-lib-seat && touch $CRON_PATH/root && chmod +x $CRON_PATH/root

WORKDIR /crontab-ui

LABEL maintainer = "@PTYin"
LABEL description = "SDU-LIB-SEAT docker"

RUN   sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
      && apk --update --no-cache add \
      wget \
      curl \
      nodejs \
      npm \
      supervisor \
      tzdata  \
      python3  \
      && ln -sf python3 /usr/bin/python \
      && python3 -m ensurepip \
      && pip3 install --no-cache --upgrade pip setuptools

COPY ./crontab-ui/supervisord.conf  /etc/supervisord.conf
COPY ./crontab-ui                   /crontab-ui
COPY ./requirements.txt             /crontab-ui/requirements.txt

RUN   npm install && pip3 install -r requirements.txt

COPY ./src/main                     /sdu

RUN  ln -s /usr/bin/node /usr/local/bin/node

ENV   HOST 0.0.0.0

ENV   PORT 8000

ENV   CRON_IN_DOCKER true

EXPOSE $PORT

CMD ["supervisord", "-c", "/etc/supervisord.conf"]