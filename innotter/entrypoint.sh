#!/bin/bash

set -e

if [ "$DATABASE" = "PGSQL" ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
