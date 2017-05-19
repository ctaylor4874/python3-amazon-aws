class ItemSearchError(ValueError):

    def __init__(self, code, message, *args, **kwargs):
        self.message = message
        self.code = code
        super(ValueError, self).__init__(message, *args, **kwargs)

    @classmethod
    def from_element(cls, e, *args, **kwargs):
        return cls(e.code, e.message, *args, **kwargs)


class SignatureDoesNotMatchError(ItemSearchError):
    pass


class RequestThrottledError(ItemSearchError):
    pass


class RequestExpiredError(ItemSearchError):
    pass


ERROR_CLASSES = {
    'SignatureDoesNotMatch': SignatureDoesNotMatchError,
    'RequestThrottled': RequestThrottledError,
    'RequestExpired': RequestExpiredError,
}


def get_error(code):
    if code in ERROR_CLASSES:
        return ERROR_CLASSES[code]
    return ItemSearchError