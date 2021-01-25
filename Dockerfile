# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.7-buster

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/ui
RUN mkdir -p /opt/app/Back-Exam
COPY requirements.txt start-server.sh /opt/app/
COPY Back-Exam /opt/app/Back-Exam/
COPY ui /opt/app/ui/

# change wordkdir
WORKDIR /opt/app

#venv
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
COPY django_grpc_framework venv/lib/python3.7/site-packages/
RUN chown -R www-data:www-data ui Back-Exam

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
