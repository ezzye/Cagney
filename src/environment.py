import os


class Environment(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def load(self, name, required=True):
        var = os.environ.get(name, None)
        if not var and required:
            raise AttributeError(f'Environment variable: \'{name}\' is missing')
        self.__dict__[name] = var
        return self

    def __getattr__(self, item):
        return self.__dict__.get(item, '')

    def __setattr__(self, key, value):
        self.__dict__.update(**{key: value})

    def __str__(self):
        return f'Environment{vars(self)}'

    __repr__ = __str__


env = (Environment()
       .load('BAD_MESSAGE_QUEUE_URL')
       .load('INPUT_QUEUE_ARN')
       .load('OUTPUT_TOPIC_ARN')
       .load('SNS_ENDPOINT', required=False)
       .load('SQS_ENDPOINT', required=False))

