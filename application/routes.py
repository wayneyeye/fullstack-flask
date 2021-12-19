import os
from flask.helpers import send_from_directory, url_for
from werkzeug.utils import redirect, secure_filename
from application import app,dynamo
from application.forms import LoginForm, RegisterForm
from application.fileserver import getFolder,allowed_file,ALLOWED_EXTENSIONS, upload_file,delete_file
from flask import render_template,Response,request,flash,send_from_directory,flash,safe_join,redirect,session
import json
from boto3.dynamodb.conditions import Key
from werkzeug.security import generate_password_hash, check_password_hash
# all routes are defined here
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",authed=True,index=True)

@app.route("/login",methods=["GET","POST"])
def login():
    if session.get("email"):
        return redirect(url_for('index'))
    form=LoginForm()
    form.validate()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        table=dynamo.tables["users"]
        user=table.query(
        KeyConditionExpression=Key('email').eq(email)
        ).get("Items")
        if user and check_password_hash(user[0]['password'],password):
            flash("You are successfully logged in!",category="success")
            session["email"]=email
            session["first_name"]=user[0]['first_name']
            return redirect(url_for("index"))
        else:
            flash("Sorry, something went wrong",category="danger")
    return render_template("login.html",login=True,form=form,title="Login")

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    if not session.get("email"):
        return redirect(url_for('login'))
    courseData=dynamo.tables['courses'].scan()['Items']
    return render_template("courses.html",courses=True,courseData=courseData,term=term)

@app.route("/register",methods=["GET","POST"])
def register():
    if session.get("email"):
        return redirect(url_for('index'))
    form=RegisterForm()
    # form.validate()
    print("befor validate on submit")
    if form.validate_on_submit():
        email=form.email.data
        # print("email="+email)
        # print("clear text:"+form.password.data)
        hashed_password=generate_password_hash(form.password.data)
        # print("hashed:"+hashed_password)
        form.password=hashed_password
        form.save()
        flash("You are successfully registered!",category="success")
        return redirect(url_for('login'))
    return render_template("register.html",title="New User Registration",form=form,register=True)

@app.route("/user")
def user():
    if not session.get("email"):
        return redirect(url_for('login'))
    users=dynamo.tables['users'].scan()['Items']
    # print(users)
    return render_template("user.html",users=users,user=True)

@app.route("/logout")
def logout():
    session.pop("email")
    session.pop("first_name")
    flash("You are successfully logged out!",category="success")
    return redirect(url_for('index'))

@app.route("/confirm",methods=["POST","GET"])
def confirm():
    args=request.form
    print(args)
    return render_template("confirm.html",data=args)

@app.route("/fileserver",methods=["GET","POST"], strict_slashes=False)
@app.route('/fileserver/<path:path>',methods=["GET","POST"])
def fileserver(path=''):
    if not session.get("email"):
        return redirect(url_for('login'))
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
    if not session.get("email"):
        return redirect(url_for('login'))
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