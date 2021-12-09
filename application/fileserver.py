import os
from datetime import datetime
from flask import safe_join
ALLOWED_EXTENSIONS=['py','yaml','yml']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def upload_file(path,file):
    print("save to "+safe_join(path,file.filename))
    file.save(safe_join(path,file.filename))
def delete_file(path,file):
    print("current path "+os.getcwd())
    print("delete file "+file)
    os.remove(file)
def getFolder(path='./'):
    list = os.listdir(path)
    list.sort(key=lambda a: a)
    data=[]
    for name in list:
        fullname = safe_join('' if path=='./' else path, name)
        displayname = linkname = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            displayname = name + "/"
            linkname = name + "/"
            dir = True
        else:
            dir = False
        size=os.stat(fullname).st_size
        mtime=datetime.fromtimestamp(os.stat(fullname).st_mtime).strftime("%Y/%m/%d %H:%M:%S")
        data.append({
        "name":name,
        "fullname":fullname,
        "displayname":displayname,
        "linkname":linkname,
        "mtime":mtime,
        "size":size,
        "dir":dir})
    return data