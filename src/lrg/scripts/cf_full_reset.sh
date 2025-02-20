rm -rf ./*/migrations/0*
set -e

# Terminate active connections
psql -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();"

# Drop and recreate the database
psql -d postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};"
psql -d postgres -c "CREATE DATABASE ${DB_NAME} OWNER ${PGUSER};"

python manage.py flush --no-input
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser --no-input

python manage.py add_locations
python manage.py populate