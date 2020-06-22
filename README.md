# Hatgame!

### Installing
1. install python requirements from requirements.txt

### Build the Static React Components (optional)
You only need to do this if you update anything in app/static/*
2. install npm (https://www.npmjs.com/get-npm)
3. cd project root > app > static
4. npm install --save
5. npm build

### Start the backend server
1) Open a new terminal
2) cd project root
3) export FLASK_APP=app.py
4) export FLASK_ENV=development
5) export FLASK_DEBUG=1
6) flask run
Note - you can also make a custom pycharm run configuration 
Script path: <path to flask bin - the output of 'which flask'>  
paramters: run
Environment Variables:
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1