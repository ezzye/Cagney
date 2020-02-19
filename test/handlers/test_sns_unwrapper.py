import unittest

from src.handlers.sns_unwrapper import sns_unwrapper
from src.stream.sqs_message import SqsMessage


class TestSnsUnwrapper(unittest.TestCase):

    def test_update_body(self):
        sqs_message = SqsMessage({
            'messageId': 'queue_message_id',
            'body': '{'
                    '   "Type": "Notification",'
                    '   "MessageId": "notification_message_id",'
                    '   "Message": "notification_message_body"'
                    '}',
        })

        sns_unwrapper(sqs_message)

        self.assertEqual(sqs_message['body'], 'notification_message_body')
        self.assertEqual(sqs_message['messageId'], 'queue_message_id')
