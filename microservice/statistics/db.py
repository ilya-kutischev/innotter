import boto3
from boto3.resources.base import ServiceResource


class Config:
    DB_REGION_NAME = "sus"
    DB_ACCESS_KEY_ID = "sus"
    DB_SECRET_ACCESS_KEY = "sys"


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8001',
                         region_name=Config.DB_REGION_NAME,
                         aws_access_key_id=Config.DB_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.DB_SECRET_ACCESS_KEY)

    return ddb


def generate_table():
    ddb = initialize_db()
    ddb.create_table(
        TableName='Statistics',
        AttributeDefinitions=[
            {
                'AttributeName': 'id',  # In this case, I only specified uid as partition key (there is no sort key)
                'AttributeType': 'N'  # with type string
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'id',  # attribute uid serves as partition key
                'KeyType': 'HASH'
            }
        ],

    )
    print('Successfully created table Statistics')