from flask import Flask, render_template
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('HelloIntent')
def hello(firstname):
    welcome_message = "Hi, your app is working"
    return statement(welcome_message)

if __name__ == '__main__':
    app.run(debug=True)