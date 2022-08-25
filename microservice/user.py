from botocore.exceptions import ClientError
from db import ddb
from fastapi.responses import  JSONResponse
from boto3.dynamodb.conditions import Key

table = ddb.Table("statistics")


def create_user(user: dict):
    try:
        table.put_item(Item=user)
        return user
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_user(id: str):
    try:
        response = table.query(
            KeyConditionExpression = Key("id").eq(id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_users():
    try:
        response = table.scan(
            Limit=100,
            AttributesToGet=["id","posts", "likes", "followers", "follow_requests"]
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def delete_user(user: dict):
    try:
        response=table.delete_item(
            Key={
                "id": user["id"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def update_user(user: dict):
    try:
        response = table.update_item(
            Key={
                "id": user["id"]
            },
            UpdateExpression="SET posts = :posts, likes = :likes, followers = :followers, follow_requests = :follow_requests",
            ExpressionAttributeValues={
                ":posts": user["posts"],
                ":likes": user["likes"],
                ":followers": user["followers"],
                ":follow_requests": user["follow_requests"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)