backend: gunicorn --chdir server --worker-class eventlet -w 1 -b :5000 app:app
web: node ./client/frontend.js