# First we compile the node stuff
FROM node:19-alpine as node-build
COPY ./frontend ./frontend
WORKDIR frontend

# Clean install all packages from package-lock.json, then build
RUN npm ci
RUN npm run build

# Then we run the python stuff
FROM python:3.11
COPY ./flaskr ./flaskr

# Copy pre-compiled node stuff
COPY --from=node-build ./frontend/dist ./flaskr/vite

# Install reqs
RUN pip install --upgrade pip
RUN pip install -r flaskr/requirements.txt

# Install mongodb
RUN apt update
RUN apt upgrade -y
RUN apt-get install gnupg curl
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt update
RUN apt install -y mongodb-org

# Set env variables
ARG DB_PW=
ENV DB_PASSWORD=$DB_PW

ENV DB_USERNAME=xs-bot
ENV DB_ADDRESS=cluster0.dvvipyf.mongodb.net

EXPOSE 5000
EXPOSE 27017
EXPOSE 80

CMD python -m flask --app flaskr --debug run --host 0.0.0.0 --port 80
