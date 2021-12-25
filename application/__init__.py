from flask import Flask
from flask_dynamo import Dynamo
from application import config
from flask_restx import Api
app=Flask(__name__)
api=Api()
api.init_app(app)
app.config.from_object(config.Config)
#print(app.config['DYNAMO_TABLES'])
dynamo= Dynamo(app)
with app.app_context():
    dynamo.create_all(wait=True)
    print("DynamoDB Table created")
from application import routes