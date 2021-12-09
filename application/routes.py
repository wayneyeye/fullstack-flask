from flask.helpers import send_from_directory, url_for
from werkzeug.utils import redirect, secure_filename
from application import app
from application.fileserver import getFolder,allowed_file,ALLOWED_EXTENSIONS, upload_file,delete_file
from flask import render_template,Response,request,send_from_directory,flash
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

@app.route("/fileserver",methods=["GET","POST"], strict_slashes=False)
@app.route('/fileserver/<path:path>',methods=["GET","POST"])
def fileserver(path=''):
    realpath='/'+path
    path=path or './'
    print("path=",path)
    if request.form.get("download"):
        print("FILE DOWNLOAD REQUEST: "+app.config["UPLOAD_FOLDER"]+' '+request.form.get("download"))
        # add ../ as this script is in the application folder
        return send_from_directory(app.config["UPLOAD_FOLDER"],request.form.get("download"))
    if request.form.get("delete"):
        print("FILE DELETE REQUEST: "+app.config["UPLOAD_FOLDER"]+request.form.get("delete"))
        delete_file(app.config["UPLOAD_FOLDER"],request.form.get("delete"))
        # add ../ as this script is in the application folder
        return redirect(url_for('fileserver')+'/'+path)
    if request.files.get("upload"):
        file=request.files.get("upload")
        print("UPLOAD "+file.filename)
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("FILE UPLOAD ALLOWED: "+app.config["UPLOAD_FOLDER"]+ path +' '+filename)
            upload_file(path,file)
            return redirect(url_for('fileserver')+'/'+path)
        else:
            flash(request.files.get("upload").filename+" is not in "+','.join(ALLOWED_EXTENSIONS))
            return redirect(url_for('fileserver')+'/'+path)
    else:
        return render_template("fileserver.html",fileData=getFolder(path),path=path,fileserver=True)

@app.route("/enrollment",methods=["GET","POST"])
def enrollment():
    courseID=request.form.get("courseID")
    title=request.form.get("title")
    description=request.form.get("description")
    credits=request.form.get("credits")
    term=request.form.get("term")
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