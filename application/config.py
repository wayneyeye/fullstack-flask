import os
class Config():
    SECRET_KEY=os.environ.get("SECRET_KEY") or "ajfdkajo1231"
    UPLOAD_FOLDER='../'
