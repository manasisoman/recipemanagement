# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app

# copy the content of the local src directory to the working directory
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8011

# command to run on container start
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]
