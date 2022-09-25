import boto3

def send_follow_email():
    ses_client = boto3.client("ses",
                              region_name="us-west-2",
                              aws_access_key_id="suus",
                              aws_secret_access_key="sus",
                              endpoint_url="http://localhost:4566")
    ses_client.verify_email_identity(EmailAddress="innotter@gmail.com")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "kutischev10@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello, see a new post!",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Visit your innotter page",
            },
        },
        Source="innotter@gmail.com",
    )


# send_plain_email()