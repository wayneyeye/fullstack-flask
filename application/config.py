import os
class Config():
    SECRET_KEY=os.environ.get("SECRET_KEY") or "8d094ae09b7cb0053b35c25a9d25d2dbc8c08b6074dd1eb55f690833aea8b750"
    AWS_REGION="us-west-2"
    AWS_PROFILE="wenhe"
    DYNAMO_TABLES=[
    dict(
         TableName='users',
         KeySchema=[dict(AttributeName='email', KeyType='HASH')],
         AttributeDefinitions=[dict(AttributeName='email', AttributeType='S')],
         ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    ), 
    dict(
         TableName='courses',
         KeySchema=[dict(AttributeName='courseID', KeyType='HASH')],
         AttributeDefinitions=[dict(AttributeName='courseID', AttributeType='S')],
         ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    ), 
    dict(
         TableName='enrollment',
         KeySchema=[dict(AttributeName='email', KeyType='HASH'),dict(AttributeName='courseID', KeyType='RANGE')],
         AttributeDefinitions=[dict(AttributeName='email', AttributeType='S'),dict(AttributeName='courseID', AttributeType='S')],
         ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
]
    SERVING_FOLDER=os.getcwd()+'/ftp_folder'
