#!/bin/bash
cd /home/site/wwwroot/src
gunicorn ProyectoSITU.wsgi --bind 0.0.0.0:8000 --timeout 600
