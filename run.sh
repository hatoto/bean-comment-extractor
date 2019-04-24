#!/bin/sh

#export FLASK_APP=main.py
#python -m flask run -h 0.0.0.0 -p 11082 >> logParser.log 2>&1 &

gunicorn -w 1 -c config.py  main:app