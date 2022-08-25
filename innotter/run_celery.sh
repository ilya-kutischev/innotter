#!/bin/sh

sleep 5

pipenv run celery -A innotter worker -l info
