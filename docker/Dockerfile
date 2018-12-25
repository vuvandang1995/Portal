FROM python:3
MAINTAINER dangvv
ENV PYTHONUNBUFFERD 1
RUN apt-get update && apt-get install -y supervisor
RUN apt-get install -y python3-pip
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/
COPY intercom.CERT.crt /etc/ssl/certs/
COPY intercom.vn.PRIVATE.key /etc/ssl/private/
RUN mkdir /home/kvmvdi
WORKDIR /home/kvmvdi
ADD requirements.txt /home/kvmvdi/
RUN pip3 install -r requirements.txt
RUN pip3 uninstall -y redis
RUN pip3 install redis==2.10.6
CMD ["/usr/bin/supervisord"]
