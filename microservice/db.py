from boto3 import resource
import os
from dotenv import load_dotenv, find_dotenv


class Config:
    load_dotenv(find_dotenv())
    DB_REGION_NAME = os.environ["DB_REGION_NAME"]
    DB_ACCESS_KEY_ID = os.environ["DB_ACCESS_KEY_ID"]
    DB_SECRET_ACCESS_KEY = os.environ["DB_SECRET_ACCESS_KEY"]


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
    "ProvisionedThroughput" : {
        'ReadCapacityUnits': 10,
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
            )
    except Exception as e:
        print(e)