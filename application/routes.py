from application import app
from flask import render_template,Response,request
import json
# all routes are defined here
courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",authed=True,index=True)

@app.route("/login")
def login():
    return render_template("login.html",login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html",courses=True,courseData=courseData,term=term)

@app.route("/register")
def register():
    return render_template("register.html",register=True)

@app.route("/enrollment")
def enrollment():
    courseID=request.args.get("courseID")
    title=request.args.get("title")
    description=request.args.get("description")
    credits=request.args.get("credits")
    term=request.args.get("term")
    return render_template("enrollment.html",enrollment=True,data={
        "courseID":courseID,
        "title":title,
        "description":description,
        "credits":credits,
        "term":term
        })

@app.route("/api")
@app.route("/api/<idx>")
def api(idx=None):
    if idx is None:
        jdata=courseData
    else:
        jdata=courseData[int(idx)]
    return Response(json.dumps(jdata),mimetype="application/json")