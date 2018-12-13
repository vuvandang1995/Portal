FROM nginx

RUN apt-get install -y libffi-dev libssl-dev
ADD default.conf etc/nginx/conf.d/default.conf
RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
COPY intercom.CERT.crt /etc/ssl/certs/
COPY intercom.vn.PRIVATE.key /etc/ssl/private/
COPY self-signed.conf /etc/nginx/snippets/
COPY ssl-params.conf /etc/nginx/snippets/