import unittest
from src.handlers.amend_subject import amend_subject
from src.stream.sqs_message import SqsMessage


class TestCagney(unittest.TestCase):

    # def setUp(self) -> None:
    #     self.undertest = AmendmentHandler()

    def test_adding_tags_to_subject(self):
        body = {'post_code': 'E5 0SB', 'body': 'this is my emails message', 'first_name': 'Firstname',
                'last_name': 'Lastname', 'email_address': 'email.address@myemail.com',
                'email_subject': 'this is my email subject', 'mp_ref': 'ref123456', 'subject': 'Visa',
                'type': 'Policy'}
        sqs_message = SqsMessage(
            {
                'messageId': 'messageId',
                'body': body
            }
        )
        actual_body = amend_subject(sqs_message)['body']
        expected_body = {
            'post_code': 'E5 0SB',
            'body': 'this is my emails message',
            'email_address': 'email.address@myemail.com',
            'email_subject': '#Policy #Visa #ref123456 #Firstname_Lastname this is my email subject'
        }

        self.assertEqual(actual_body, expected_body)
