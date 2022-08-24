import boto3
from boto3 import resource
from os import getenv


class Config:
    # DB_REGION_NAME = getenv("DB_REGION_NAME")
    # DB_ACCESS_KEY_ID = getenv("DB_ACCESS_KEY_ID")
    # DB_SECRET_ACCESS_KEY = getenv("DB_SECRET_ACCESS_KEY")

    DB_REGION_NAME = "us-west-2"
    DB_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    DB_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def initialize_db():
    ddb = resource(
                        'dynamodb',
                         endpoint_url='http://dynamodb:8000',
                         region_name=Config.DB_REGION_NAME,
                         aws_access_key_id=Config.DB_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY
                         )

    return ddb

ddb = initialize_db()


tables = [
    {
    "TableName": "statistics",
    "KeySchema" : [
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
    ],
    "AttributeDefinitions":[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            }
        ],
    "ProvisionedThroughput" : {  # specying read and write capacity units
        'ReadCapacityUnits': 10,  # these two values really depend on the app's traffic
        'WriteCapacityUnits': 10
}
    }
]


def create_tables(ddb=ddb):
    try:
        for table in tables:
            ddb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
                ProvisionedThroughput=table["ProvisionedThroughput"],
                # BillingMode='PAY_PER_REQUEST'
            )
    except Exception as e:
        print(e)