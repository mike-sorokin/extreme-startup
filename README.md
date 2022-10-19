# Extreme Restartup

## User guide
If you are simply wanting to play Extreme (Re)Startup, go to https://extreme-restartup.fly.dev/. Hopefully it's up when you navigate to it!
### Docker
Run this if you just want to run it locally. This will 99.99% work if you have [Docker installed](https://docs.docker.com/engine/install/)
```
docker build -t se-xp .
docker run -i -t -p80:5000 se-xp
```
The server should be live on localhost.
### Manual
Run this if you don't want to install Docker (for whatever reason).
```
# Starting from project root folder
# Build static files
cd frontend
npm ci
npm run build

# Launch flask server
cd ..
python3 -m venv env
source env/bin/activate
pip install -r flaskr/requirements.txt
flask --app flaskr --debug run
```
The server should be live on localhost:5000