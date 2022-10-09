#!/bin/bash

DIR="/home/ubuntu/server/"
APP="wsgi:app"
PID="pid_file"
ADDRESS="0.0.0.0:80"
WRK_COUNT=5

sudo gunicorn --chdir $DIR --workers $WRK_COUNT --bind $ADDRESS --pid $PID $APP