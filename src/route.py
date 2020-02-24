import json
import logging

import boto3
from src.environment import env
from src.handlers.amend_subject import amend_subject
from src.handlers.sns_handler import SNSHandler
from src.handlers.bad_message_handler import BadMessageHandler
from src.stream.stream import Stream
from src.stream.sqs_message import SqsMessage
from src.handlers.sns_unwrapper import sns_unwrapper
from src.handlers.json import Json

LOGGER = logging.getLogger()
COMPONENT_NAME = 'cagney'


def handler(event, lambda_context):
    log_event_info(event, lambda_context)
    return (Stream(event['Records'])
            .add_exception_handler(bad_message_handler, json.JSONDecodeError)
            .map(SqsMessage)
            .map(sns_unwrapper)
            .map(Json.parse_body)
            .map(amend_subject)
            .map(Json.unparse_body)
            .foreach(sns_handler.send))


def log_event_info(event, context):
    LOGGER.info(f'EVENT: {event}')
    LOGGER.info(f'CONTEXT: {vars(context)}')
    LOGGER.info(f'ENVIRONMENT: {env}')


# Define variables outside of function where possible to take advantage of execution
# context reuse. This saves execution time and cost.
# (ref: https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
sqs_client = boto3.client('sqs', endpoint_url=env.SQS_ENDPOINT)

sns_client = boto3.client('sns', endpoint_url=env.SNS_ENDPOINT)

sns_handler = SNSHandler(sns_client, env.OUTPUT_TOPIC_ARN)

bad_message_handler = BadMessageHandler(
    COMPONENT_NAME,
    sqs_client,
    env.BAD_MESSAGE_QUEUE_URL,
    env.INPUT_QUEUE_ARN
)
