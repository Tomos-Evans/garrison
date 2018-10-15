#!/bin/sh
flask db upgrade
python generate_dispensers.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - garrison:app
