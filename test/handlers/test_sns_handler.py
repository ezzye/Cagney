import unittest
from unittest.mock import Mock

from src.handlers.sns_handler import SNSHandler
from src.stream.sqs_message import SqsMessage

MESSAGE_ID = 'some-id'
OUTPUT_TOPIC_ARN = 'arn:aws:sqs:eu-west-1:000000000000:IntModavHelloWorldResources-OutputTopic'


class TestSendToOutputTopic(unittest.TestCase):

    def setUp(self):
        self.mock_sns_client = Mock()
        self.mock_sns_client.publish.return_value = {'MessageId': MESSAGE_ID}
        self.under_test = SNSHandler(self.mock_sns_client, OUTPUT_TOPIC_ARN)

    def test_sends_message_to_output_topic(self):
        sqs_message = SqsMessage({
            'body': 'some-body'
        })
        self.under_test.send(sqs_message)
        self.mock_sns_client.publish.assert_called_once_with(
            TargetArn=OUTPUT_TOPIC_ARN,
            Message=sqs_message['body']
        )
