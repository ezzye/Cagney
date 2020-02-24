
class SNSHandler:

    def __init__(self, sns_client, topic_arn):
        self.sns_client = sns_client
        self.topic_arn = topic_arn

    def send(self, sqs_message):
        result = self.sns_client.publish(TargetArn=self.topic_arn, Message=sqs_message['body'])
        return sqs_message
