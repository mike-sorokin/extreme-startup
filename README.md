# Extreme Restartup

>If you are developing the project and want to see how to run it locally, scroll to the end pls

If you are simply wanting to play Extreme (Re)Startup, go to https://extreme-startup.fly.dev/. Hopefully it's up when you navigate to it!

### Docker

> THIS IS BROKEN RIGHT NOW, PLEASE REFER TO MANUAL!

Run this if you just want to run it locally. This will 99.99% work if you have [Docker installed](https://docs.docker.com/engine/install/)
```
docker build -t se-xp .
docker run -i -t -p80:5000 se-xp
```
The server should be live on localhost.
### Manual
Run this if you don't want to install Docker

Make sure there is a MongoDB daemon running on 27017.

```
# Starting from project root folder
# Build static files
cd frontend
npm ci
npm run build
mv dist ../flaskr/vite

# Launch flask server
cd ..
python3 -m venv env
source env/bin/activate
pip install -r flaskr/requirements.txt
flask --app flaskr --debug run
```
The server should be live on localhost:5000

## Developer guide
To see instant changes to both front and backend, follow this guide.
##### Terminal 1 - Flask server
This launches the Flask backend on **localhost:5000**. When deploying, you should have built the frontend stuff and this server would immediately serve it, but this takes an eternity, so we don't do it here. This server will **only** serve /api requests for your frontend. You can watch this terminal for any requests the frontend sends to the backend.
```
python3 -m venv env
source env/bin/activate
pip install -r flaskr/requirements.txt
flask --app flaskr --debug run
```
##### Terminal 2
WARNING: If you use WSL, make sure the project is in the Linux file directory, not the Windows one. Otherwise it doesn't live update for some reason.

This launches the React app on **localhost:5173**, which lets you see the UI updates as soon as you edit the source. Its interactions with the API on port 5000 should work.
```
cd frontend
npm ci  // Note - this needs to be ran only when new packages are added
npm run dev
```
