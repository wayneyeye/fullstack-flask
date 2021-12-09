import os
class Config():
    SECRET_KEY=os.environ.get("SECRET_KEY") or "8d094ae09b7cb0053b35c25a9d25d2dbc8c08b6074dd1eb55f690833aea8b750"
    AWS_REGION="eu-west-1"
    DYNAMO_TABLES=[
    dict(
         TableName='users',
         KeySchema=[dict(AttributeName='username', KeyType='HASH')],
         AttributeDefinitions=[dict(AttributeName='username', AttributeType='S')],
         ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    ), dict(
         TableName='groups',
         KeySchema=[dict(AttributeName='name', KeyType='HASH')],
         AttributeDefinitions=[dict(AttributeName='name', AttributeType='S')],
         ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    )
]
     