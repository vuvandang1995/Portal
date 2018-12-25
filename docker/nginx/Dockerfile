#FROM ubuntu:16.04
#FROM marvambass/nginx-ssl-secure
#FROM valian/docker-nginx-auto-ssl
FROM nginx

ENV LANG C.UTF-8
RUN apt-get update; apt-get install -y openssl ping curl
#CMD ["nginx"]

#RUN apt-get update -y 
#RUN apt-get upgrade -y 
#RUN apt-get install -y nginx openssl libffi-dev libssl-dev

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
COPY intercom.CERT.crt /etc/ssl/certs/
COPY intercom.vn.PRIVATE.key /etc/ssl/private/
COPY self-signed.conf /etc/nginx/snippets/
COPY ssl-params.conf /etc/nginx/snippets/
ADD default.conf etc/nginx/conf.d/default.conf

#CMD ["nginx", "-g", "daemon off;"]
