#!/bin/bash

if [ "$FULL_RESET_DB" = "True" ]; then
    echo "Resetting all data in database..."
    scripts/full_reset.sh
else
    echo "Database reset skipped."
fi
python manage.py runserver 0.0.0.0:8080
# gunicorn lrg.wsgi:application --bind 0.0.0.0:8080