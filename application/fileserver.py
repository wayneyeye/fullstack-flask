import os
from datetime import datetime
def getFolder(path='./'):
    list = os.listdir(path)
    list.sort(key=lambda a: a)
    data=[]
    for name in list:
        fullname = os.path.join(path, name)
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