from application import app
from flask import render_template
# all routes are defined here
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")