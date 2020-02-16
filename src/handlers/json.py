import json


class Json(object):

    @staticmethod
    def parse_body(sqs_message):
        return sqs_message.apply(json.loads, 'body')

    @staticmethod
    def unparse_body(sqs_message):
        return sqs_message.apply(json.dumps, 'body')
