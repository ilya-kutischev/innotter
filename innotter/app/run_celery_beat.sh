#!/bin/sh

sleep 10

su -m myuser -c "rm /tmp/celerybeat-doshi.pid > /dev/null"

su -m myuser -c "celery beat -A *.celery -l info --pidfile=/tmp/*.pid"
