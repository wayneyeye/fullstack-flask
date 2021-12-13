from application import dynamo
import json
users=json.load(open("model/users.json"))
for u in users:
    dynamo.tables['users'].put_item(Item=u)

courses=json.load(open("model/courses.json"))
for c in courses:
    dynamo.tables['courses'].put_item(Item=c)