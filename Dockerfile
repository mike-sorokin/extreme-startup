FROM python:3

COPY . .

# Update packages
RUN apt-get -y update
RUN apt-get -y upgrade

# Install reqs
RUN pip install --upgrade pip
RUN pip install -r flaskr/requirements.txt

EXPOSE 80

CMD python -m flask --app flaskr --debug run --host 0.0.0.0 --port 80
