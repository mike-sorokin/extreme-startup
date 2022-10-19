# First we compile the node stuff
FROM node:16-alpine as node-build
COPY ./frontend .

# Clean install all packages from package-lock.json, then build
RUN npm ci
RUN npm run build

# Then we run the python stuff
FROM python:3
COPY ./flaskr ./flaskr

# Copy pre-compiled node stuff
COPY --from=node-build ./build ./flaskr

# Install reqs
RUN pip install --upgrade pip
RUN pip install -r flaskr/requirements.txt

EXPOSE 5000

CMD python -m flask --app flaskr --debug run --host 0.0.0.0