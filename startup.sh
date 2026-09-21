#!/bin/bash
set -e

# Install Microsoft ODBC Driver for SQL Server if not already present.
# pyodbc/mssql-django need this OS-level driver, not just the Python package.
if ! odbcinst -q -d -n "ODBC Driver 18 for SQL Server" >/dev/null 2>&1; then
    curl -sSL -O https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb
    dpkg -i packages-microsoft-prod.deb
    apt-get update
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev
    rm -f packages-microsoft-prod.deb
fi

python manage.py collectstatic --noinput
python manage.py migrate --noinput

gunicorn webanalytics.wsgi --bind=0.0.0.0:8000
