#!/bin/bash

# Build the project
echo "Building the project..."
python3.12 -m pip install -r requirements.txt

# Make migrations
echo "Making migrations..."
python3.12 manage.py makemigrations --noinput
python3.12 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear