#!/usr/bin/env python
from flask import Flask, render_template, request
import get_data
import logging

app = Flask(__name__)
@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('landing.html',page_title="Greeting Form")

def add_to_card(t):
    return t


@app.route("/gresponse")
def greet_response_handler():
    # if form filled in, greet them using this data
    greet_types = request.args.getlist('greet_type')
    app.logger.info(greet_types)
    data = get_data.get_reddit_posts()
    yee =get_data.get_image_list(data)
    return render_template('feed.html',page_title="mEmEs",
    greetings=[add_to_card(t) for t in yee])

if __name__ == "__main__":
    # Used when running locally only.
    # When deploying to Google AppEngine, a webserver process will
    # serve your app.
    app.run(host="localhost", port=5000, debug=True)