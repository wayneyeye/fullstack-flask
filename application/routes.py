import os
from flask.helpers import send_from_directory, url_for
from werkzeug.utils import redirect, secure_filename
from application import app,dynamo
from application.forms import LoginForm, RegisterForm
from application.fileserver import getFolder,allowed_file,ALLOWED_EXTENSIONS, upload_file,delete_file
from flask import render_template,Response,request,send_from_directory,flash,safe_join
import json
# all routes are defined here
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",authed=True,index=True)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    return render_template("login.html",login=True,form=form,title="Login")

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    courseData=dynamo.tables['courses'].scan()['Items']
    return render_template("courses.html",courses=True,courseData=courseData,term=term)

@app.route("/register")
def register():
    return render_template("register.html",register=True)

@app.route("/user")
def user():
    users=dynamo.tables['users'].scan()['Items']
    # print(users)
    return render_template("user.html",users=users,user=True)

@app.route("/confirm",methods=["POST","GET"])
def confirm():
    args=request.form
    print(args)
    return render_template("confirm.html",data=args)

@app.route("/fileserver",methods=["GET","POST"], strict_slashes=False)
@app.route('/fileserver/<path:path>',methods=["GET","POST"])
def fileserver(path=''):
    path=path
    print("path=",path)
    # download file from FTP
    if request.form.get("download"):
        print("FILE DOWNLOAD REQUEST: "+request.form.get("download"))
        print("PARENT FOLDER" + app.config["SERVING_FOLDER"])
        # add ../ as this script is in the application folder
        return send_from_directory(app.config["SERVING_FOLDER"],request.form.get("download"),mimetype='application/octet-stream')
    if request.form.get("delete"):
        print("FILE DELETE REQUEST: "+app.config["SERVING_FOLDER"]+request.form.get("delete"))
        delete_file(safe_join(app.config["SERVING_FOLDER"],request.form.get("delete")))
        # add ../ as this script is in the application folder
        return redirect(url_for('fileserver')+'/'+path)
    # upload file from local
    if request.files.get("upload"):
        file=request.files.get("upload")
        print("UPLOAD "+file.filename)
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("FILE UPLOAD ALLOWED: "+safe_join(app.config["SERVING_FOLDER"],path,filename))
            upload_file(safe_join(app.config["SERVING_FOLDER"],path),file)
            return redirect(url_for('fileserver')+'/'+path)
        else:
            flash(request.files.get("upload").filename+" is not in "+','.join(ALLOWED_EXTENSIONS))
            return redirect(url_for('fileserver')+'/'+path)
    else:
        print("path = "+ path)
        return render_template("fileserver.html",fileData=getFolder(safe_join(app.config["SERVING_FOLDER"],path),relative_path=path),path=path,fileserver=True)

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