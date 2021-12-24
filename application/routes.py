import os
import json
from flask.helpers import send_from_directory, url_for
from flask import render_template,Response,request,flash,send_from_directory,flash,safe_join,redirect,session
from werkzeug.utils import redirect, secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from boto3.dynamodb.conditions import Key
from application import app,dynamo
from application.forms import LoginForm, RegisterForm,EnrollmentForm
from application.fileserver import getFolder,allowed_file,ALLOWED_EXTENSIONS, upload_file,delete_file

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
    form=EnrollmentForm()
    # get course list from dynamoDB
    courseData=dynamo.tables['courses'].scan()['Items']
    return render_template("courses.html",courses=True,form=form,courseData=courseData,term=term)

@app.route("/register",methods=["GET","POST"])
def register():
    if session.get("email"):
        return redirect(url_for('index'))
    form=RegisterForm()
    # form.validate()
    # print("before validate on submit")
    if form.validate_on_submit():
        email=form.email.data
        hashed_password=generate_password_hash(form.password.data)
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

@app.route("/enrollment",methods=["GET","POST"])
def enrollment():
    if not session.get("email"):
        return redirect(url_for('login'))
    form=EnrollmentForm()
    email=session.get("email")
    courseID=form.courseID.data
    if courseID: # if is a enrollment submit
        # get course detail
        if form.validate_on_submit():
            courseData=dynamo.tables['courses'].query(
            KeyConditionExpression=Key('courseID').eq(courseID)
            )['Items']
            # update to the backend db
            form.email=email
            form.save()
            return render_template("enrollment.html",title="You have successfully enrolled in the course!",enrollment=True,data=courseData)
    else: # if is to query the enrolled courses
        # get enrolled courseIDs
        courseIDs=dynamo.tables['enrollment'].query(
        KeyConditionExpression=Key('email').eq(email)
        )['Items']
        courseIDs=(list(map(lambda a:a['courseID'],courseIDs)))
        enrollmentdata=[]
        # iterate thru courseIDs and get detailed course info
        for id in courseIDs:
            enrollmentdata=enrollmentdata+dynamo.tables['courses'].query(
            KeyConditionExpression=Key('courseID').eq(id)
            )['Items']
        # render title based on existence of results
        title = "Here is a list of your enrolled courses" if enrollmentdata else "You haven't enrolled in any courses"
        return render_template("enrollment.html",title=title,data=enrollmentdata,enrollment=True)

@app.route("/api")
@app.route("/api/<idx>")
def api(idx=None):
    courseData=dynamo.tables['courses'].scan()['Items']
    if idx is None:
        jdata=courseData
    else:
        jdata=courseData[int(idx)]
    return Response(json.dumps(jdata),mimetype="application/json")

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
