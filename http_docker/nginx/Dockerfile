FROM nginx

ENV LANG C.UTF-8
RUN apt-get update; apt-get install -y curl
ADD default.conf etc/nginx/conf.d/default.conf
