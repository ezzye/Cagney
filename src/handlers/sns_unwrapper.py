import json
import logging

LOGGER = logging.getLogger()


def sns_unwrapper(sqs_message):
    try:
        sns_message = json.loads(sqs_message['body'])
    except json.JSONDecodeError:
        LOGGER.info("SQS message is non-json; not an SNS message.")
        # An SNS message should always be a JSON object
        # So this is not an SNS message. Return SQS message (do nothing)
        return sqs_message

    if sns_message.get('Type', None) != 'Notification':
        LOGGER.info("SQS message does not have type notification; not an SNS message.")
        # Even if it is JSON, it still may not be an SNS message.
        # An SNS message should always have 'Type': 'Notification'
        return sqs_message

    # Now sns message info can be extracted and used to modify the sqs message

    sqs_message['body'] = sns_message['Message']
    return sqs_message
