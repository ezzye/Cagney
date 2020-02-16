class Stream(object):

    def __init__(self, iterable: iter):
        self._iterable = iterable
        self._exception_handlers = {}

    def foreach(self, handler):
        try:
            for item in self._iterable:
                self._safe_handle(handler, item)
        except StopStreamIteration:
            pass

    def collect(self, handler):
        return self._safe_handle(handler, self._iterable)

    def map(self, handler):
        self._iterable = (self._safe_handle(handler, item)
                          for item in self._iterable)
        return self

    def filter(self, handler):
        self._iterable = (item for item in self._iterable
                          if self._safe_handle(handler, item))
        return self

    def flatmap(self, handler):
        self.map(handler)
        self._iterable = flatten(self._iterable)
        return self

    def add_exception_handler(self, handler, *exceptions):
        for e in exceptions:
            self._exception_handlers[e] = handler
        return self

    def _handled_exceptions(self):
        return tuple(self._exception_handlers)

    def _safe_handle(self, handler, item):
        try:
            return handler(item)
        except self._handled_exceptions() as e:
            self._get_exception_handler(e.__class__)(e, item)
            raise StopStreamIteration()

    def _get_exception_handler(self, exception_type):
        if exception_type in self._exception_handlers:
            return self._exception_handlers[exception_type]
        # Except blocks match subclasses we might not have a key for
        # the exception in self._exception_handlers; therefore, we need
        # to find the parent type of this exception
        for handled_type in self._exception_handlers:
            if issubclass(exception_type, handled_type):
                return self._exception_handlers[handled_type]


class StopStreamIteration(StopIteration):
    """
    Subclasses StopIteration to avoid ambiguity between unhandled exceptions and
    user defined handlers.
    """
    pass


def flatten(iterable):
    return (item for sub_iter in iterable for item in sub_iter)
