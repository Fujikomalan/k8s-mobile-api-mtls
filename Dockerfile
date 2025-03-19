FROM python:3.8-alpine


RUN apk update && apk add --no-cache \
    nginx \
    supervisor

RUN mkdir /var/flaskapp/ \
    /etc/supervisor.d/ \
    /etc/nginx/ssl/ 

COPY ./nginx/ /etc/nginx/http.d/

COPY ./flask/ /var/flaskapp/

COPY ./supervisord/ /etc/supervisor.d/

RUN pip3 install -r /var/flaskapp/requirements.txt

WORKDIR /var/flaskapp/

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
