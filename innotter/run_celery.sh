#!/bin/sh

sleep 10

celery -A innotter worker -l info
