FROM python:3

# Update packages
RUN apt-get -y update
RUN apt-get -y upgrade

# Install flask, set environment variables for our app
RUN apt-get -y install python3-flask
ENV FLASK_APP=simpleFlask.py
ENV FLASK_ENV=development

COPY . .

EXPOSE 80

CMD flask run --host 0.0.0.0 --port 80
