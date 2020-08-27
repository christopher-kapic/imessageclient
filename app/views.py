from app import app

from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/init")
def load_init():
    # This function needs to return the JSON document with all of the conversations. I'm not sure the best way to do that (whether I should restructure/copy/paste the code you've written or if I should call IanCode.py)
    return "This is a string, but we need it to be the JSON."
