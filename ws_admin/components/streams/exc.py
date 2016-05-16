from ikcms.ws_apps.composite.exc import BaseError, FieldRequiredError


class StreamBaseError(BaseError):

    def __init__(self, stream):
        self.stream = stream


class StreamNotFound(StreamBaseError):
    message = 'Stream not found'

    def __init__(self, stream):
        self.stream = stream

    def __str__(self):
        return '{}: stream={}'.format(
            self.message,
            self.stream,
    )


class ActionNotFound(StreamBaseError):
    message = 'Action not found'

    def __init__(self, stream, action):
        self.stream = stream
        self.action = action

    def __str__(self):
        return '{}: stream={}, action={}'.format(
            self.message,
            self.stream,
            self.action,
    )

