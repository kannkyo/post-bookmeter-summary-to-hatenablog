import boto3
import base64
import logging
import json

logger = logging.getLogger()

region_name = "ap-northeast-1"


def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])

    secret = json.loads(secret)

    logger.info(f"get secret={secret_name}")
    logger.debug(secret)

    return secret
