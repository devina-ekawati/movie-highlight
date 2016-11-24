#!/usr/bin/env bash
export HTTP_PROXY=http://167.205.22.102:8800
export HTTPS_PROXY=http://167.205.22.102:8800

export FLASK_APP=Web.py
flask run --host=0.0.0.0 --port=5002
