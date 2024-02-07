class IcometrixException(Exception):
    pass


class IcometrixHttpException(IcometrixException):
    fmt = "An HTTP Client raised an unhandled exception: {error}"


class IcometrixParseException(IcometrixException):
    fmt = "Failed to parse HTTP response body"


class IcometrixConfigException(IcometrixException):
    fmt = "Invalid configuration"


class IcometrixAuthException(IcometrixException):
    fmt = "Authentication failed"
