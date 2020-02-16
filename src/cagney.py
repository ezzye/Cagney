import json
import logging

import boto3
from src.environment import env
from src.handlers.sns_handler import SNSHandler
from src.handlers.bad_message_handler import BadMessageHandler

LOGGER = logging.getLogger()
COMPONENT_NAME = 'cagney'


def handler(event, lambda_context):
    log_event_info(event, lambda_context)
    pass


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


