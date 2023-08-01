class BeforeAllException(Exception):
    def __init__(self, **kwargs):
        self.code = kwargs.get("code", 400)
        self.key_path = kwargs.get("key_path", "unknown")
        self.message = kwargs.get("message", "internal server error")
        super().__init__(self.message)


class ApiTimeout(Exception):
    """
    Raised when we know our endpoint will timeout, but catch it so to return to the user a better error message than
    502, internal server error.
    """

    pass
