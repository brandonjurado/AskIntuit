# AskIntuit
Answers questions directed towards Intuit Knowledge Base via Alexa skill and/or web interface

- Branches:
  - Master: React web application
  - VoiceInterface: Source code used to create an Alexa skill
  - questionsAndAnswers: Web scraper backend used in both web application and Alexa skill

## Setting up environment for React web interface
Ensure you have all the correct dependancies installed:

**pip MUST be 9.0.1 or lower**
```
sudo easy_install pip
```
**Now we are going to setup the Flask web framework:**
```
pip install Flask
pip install flask-ask
pip install virtualenv
pip install --upgrade pip setuptools
```

**Following, we will set up webpack:**
```
npm install webpack@3.0.0 -g
# Run below command within app/static/js
npm install
npm i --save axios
```
**Finally, running the environment:**
In one terminal run ```webpack --watch``` and in another terminal window: ```FLASK_APP=app.py flask run```

You can now access the web application through its respective local address
