#!/bin/sh
# Exit script on error
set -e

# Run Django migrations
python /code/manage.py makemigrations || { echo "makemigrations command failed"; exit 1; }
python /code/manage.py migrate || { echo "migrate command failed"; exit 1; }

# Execute the command passed as arguments to this script
exec "$@"
