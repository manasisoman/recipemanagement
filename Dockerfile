# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app

# install git in the container
RUN apt-get update && apt-get install -y git

# clone or pull the repository from GitHub
RUN git clone https://github.com/manasisoman/recipemanagement.git /app

# switch to the desired branch (optional)
RUN git checkout veer

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8011

# command to run on container start
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]
