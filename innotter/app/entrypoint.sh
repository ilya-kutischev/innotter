#!/bin/bash

#until nc -z -v -w30 $SQL_HOST $SQL_PORT
#do
#    echo "Waiting for a database..."
#    sleep 0.5
#done



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
