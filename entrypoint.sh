#!/bin/bash

# Navigate to the app directory (already set as WORKDIR in Dockerfile)
# cd /app - This line is not necessary as WORKDIR is already /app

# Clone the repository if the /app directory is empty, else pull the latest changes
if [ -z "$(ls -A /app)" ]; then
   git clone https://github.com/manasisoman/recipemanagement.git /app
else
   git -C /app pull
fi

# Start the FastAPI application
# Replace 'yourapp.main:app' with the correct path to your FastAPI app
uvicorn main:app --host 0.0.0.0 --port 8011