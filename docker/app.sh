#!/bin/bash
if [ -n "$MODE" ] && [ "$MODE" = "PROD" ]
then gunicorn main:app -w 4 -k uvicorn_worker.UvicornWorker --bind=0.0.0.0:$API_GATEWAY_PORT
else python main.py
fi
#gunicorn main:app -w 4 -k uvicorn_worker.UvicornWorker --bind=0.0.0.0:6100
#python main.py