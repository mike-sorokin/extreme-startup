# Extreme Restartup

## How to run
If you are simply wanting to play Extreme (Re)Startup, go to https://extreme-restartup.fly.dev/. 
### Docker
Run this if you just want to run it locally.
```
docker build -t se-xp .
docker run -i -t -p80:80 se-xp
```
### Manual
Run this if you want to see live changes as you are developing code. 
```
# Build static files
cd frontend
npm ci
npm run build

# Launch flask server
cd ..
pip install -r flaskr/requirements.txt
export FLASK_APP=flaskr
export FLASK_ENV=development
python -m flask run --host 0.0.0.0 --port 80

```