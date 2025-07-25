#!/bin/bash

WORKDIR="/home/ubuntu/actions-runner/_work/G6Back/G6Back"

echo "Starting Gunicorn restart script..."

source "$WORKDIR/venv/bin/activate"

echo "VENV Activated"


sudo systemctl daemon-reload
sudo systemctl restart gunicorn

echo "Gunicorn service restarted"

sudo systemctl status gunicorn --no-pager -n 20

echo "Gunicorn restart done."
