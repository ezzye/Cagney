import logging
import traceback

import xmltodict

LOGGER = logging.getLogger()


class BadMessageHandler:

    def __init__(self, component_name, sqs_client, bad_message_queue_url, input_queue_arn):
        self.sqs_client = sqs_client
        self.bad_message_queue_url = bad_message_queue_url
        self.input_queue_arn = input_queue_arn
        self.component_name = component_name

    def __call__(self, exception, sqs_message):
        stacktrace = traceback.format_exc()
        description = str(exception)

        LOGGER.warning(f"Sending bad message: {description}\n{stacktrace}")
        bad_message_contents = {
            'badmsg': {
                'description': description,
                'sourceQueue': self.input_queue_arn,
                'component': self.component_name,
                'stacktrace': stacktrace,
                'body': sqs_message.original['body']
            }
        }
        bad_message_body = xmltodict.unparse(bad_message_contents, pretty=True)
        result = self.sqs_client.send_message(QueueUrl=self.bad_message_queue_url, MessageBody=bad_message_body)


class BadMessageException(Exception):

    def __init__(self, *args):
        Exception.__init__(self, *args)
