#!/bin/bash

VENV="/home/ubuntu/server/venv/"
ACTIVATE="$(VENV)bin/activate"

sudo apt update -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y
python3.6 -m venv $VENV
# shellcheck source=./bin/activate
source "$ACTIVATE"
pip3.6 install wheel
pip3.6 install flask
pip3.6 install gunicorn
deactivate

