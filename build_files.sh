#!/bin/bash

echo "BUILD START"

# Install Python dependencies
python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

echo "BUILD END"
