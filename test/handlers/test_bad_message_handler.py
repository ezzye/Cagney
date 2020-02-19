import unittest
from unittest.mock import Mock, patch

from src.handlers.bad_message_handler import BadMessageHandler
from src.stream.sqs_message import SqsMessage

INPUT_QUEUE_ARN = 'arn:aws:sqs:eu-west-1:000000000000:IntModavHelloWorldResources-InputQueue'
BAD_MESSAGE_QUEUE_URL = 'https://sqs.eu-west-1.amazonaws.com/000000000000/IntModavHelloWorldResources-BadMessageQueue'
MESSAGE_ID = 'some-id'


class TestBadMessageHandler(unittest.TestCase):

    def setUp(self):
        self.mock_sqs_client = Mock()
        self.mock_sqs_client.send_message.return_value = {'MessageId': MESSAGE_ID}
        self.under_test = BadMessageHandler('helloworld', self.mock_sqs_client, BAD_MESSAGE_QUEUE_URL, INPUT_QUEUE_ARN)

    @patch('src.handlers.bad_message_handler.traceback')
    def test_sends_bad_message(self, traceback):
        traceback.format_exc = Mock(return_value='some-stacktrace')
        sqs_message = SqsMessage({
            'body': 'some-body'
        })
        self.under_test(Exception(), sqs_message)

        expected_bad_message = """<?xml version="1.0" encoding="utf-8"?>
<badmsg>
\t<description></description>
\t<sourceQueue>arn:aws:sqs:eu-west-1:000000000000:IntModavHelloWorldResources-InputQueue</sourceQueue>
\t<component>helloworld</component>
\t<stacktrace>some-stacktrace</stacktrace>
\t<body>some-body</body>
</badmsg>"""

        self.mock_sqs_client.send_message.assert_called_once_with(
            QueueUrl=BAD_MESSAGE_QUEUE_URL,
            MessageBody=expected_bad_message
        )
