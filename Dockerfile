# docker run -d -p 8000:8000 ptyin/crontab-ui
FROM alpine:3.13.5

ENV CRON_PATH=/etc/crontabs
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

RUN   mkdir /crontab-ui; touch $CRON_PATH/root; chmod +x $CRON_PATH/root

WORKDIR /crontab-ui

LABEL maintainer = "@PTYin"
LABEL description = "SDU-LIB-SEAT docker"

RUN   apk --update --no-cache add \
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
COPY ./src/main                     /crontab-ui

RUN   npm install && pip3 install -r requirements.txt

ENV   HOST 0.0.0.0

ENV   PORT 8000

ENV   CRON_IN_DOCKER true

EXPOSE $PORT

CMD ["supervisord", "-c", "/etc/supervisord.conf"]