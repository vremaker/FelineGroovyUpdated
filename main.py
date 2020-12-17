#!/usr/bin/env python
from flask import Flask, render_template, request
import get_data
import random
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('landing.html',page_title="Greeting Form")

def add_to_card(t):
    return t


@app.route("/gresponse")
def greet_response_handler():
    randomChoices = ["memes", "dogs", "aardvark", "eggs", "funny", "jokes"] 
    # if form filled in, greet them using this data
    greet_types = request.args.getlist('greet_type')
    app.logger.info(greet_types)
    
    if len(greet_types) == 0:
        greet_types = randomChoices
    #  print(test.__class__.__name__)
    yee =get_data.curate_feed(greet_types)
    return render_template('feed.html',page_title="Your Personalized Feed",
    greetings=[add_to_card(t) for t in yee])


if __name__ == "__main__":
    # Used when running locally only.
    # When deploying to Google AppEngine, a webserver process will
    # serve your app.
    app.run()

