#!/bin/bash

cd /app
git pull origin veer

# Start your application
uvicorn main:app --host 0.0.0.0 --port 8011