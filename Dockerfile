FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip install flask

COPY . .

CMD python simpleFlask.py
