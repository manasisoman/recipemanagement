# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /app

# install git in the container
RUN apt-get update && apt-get install -y git

# install dependencies
# This assumes that your requirements.txt is in the context of the build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8011

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD [ "/entrypoint.sh" ]