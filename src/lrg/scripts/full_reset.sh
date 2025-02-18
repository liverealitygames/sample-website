rm -rf ./*/migrations/0*
set -e

export OWNER=lrg_demo_owners
export PGPASSWORD=$RDS_PASSWORD
export PGHOST=$RDS_HOSTNAME
export PGUSER=$RDS_USERNAME
export PGPORT=$RDS_PORT

# Terminate active connections
psql -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = '${RDS_DB_NAME}' AND pid <> pg_backend_pid();"

# Drop and recreate the database
psql -d postgres -c "DROP DATABASE IF EXISTS ${RDS_DB_NAME};"
psql -d postgres -c "CREATE DATABASE ${RDS_DB_NAME} OWNER ${OWNER};"

python manage.py flush --no-input
python manage.py makemigrations homepage && python manage.py makemigrations posts && python manage.py makemigrations community && python manage.py migrate
python manage.py createsuperuser --no-input

python manage.py add_locations
python manage.py populate