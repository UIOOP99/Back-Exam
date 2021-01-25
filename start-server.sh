#!/usr/bin/env bash

# start-server.sh
# if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
#     (cd infoBank; python manage.py createsuperuser --no-input)
# fi
(/opt/app/venv/bin/gunicorn --chdir /opt/app/Back-Exam/BackExam BackExam.wsgi:application --user www-data --bind unix:exam.sock --workers 3) & 
(/opt/app/venv/bin/python /opt/app/Back-Exam/BackExam/manage.py grpcrunserver localhost:50057) & 
(/opt/app/venv/bin/gunicorn --chdir /opt/app/ui/ui_services ui_services.wsgi:application --user www-data --bind unix:ui.sock --workers 3) & 
(/opt/app/venv/bin/python /opt/app/ui/ui_services/manage.py grpcrunserver localhost:50053) &
nginx -g "daemon off;"