import copy


class SqsMessage(dict):

    def __init__(self, record):
        super().__init__(record)
        self.original = copy.deepcopy(record)

    def apply(self, func, key):
        self[key] = func(self[key])
        return self

    def updated(self, **kwargs):
        self.update(**kwargs)
        return self
