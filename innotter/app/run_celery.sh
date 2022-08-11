#!/bin/sh

sleep 10

su -c "celery worker -A *.celery -l info"
