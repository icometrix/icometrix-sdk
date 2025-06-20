class IcometrixException(Exception):
    pass


class IcometrixHttpException(IcometrixException):
    def __init__(self, message: str, status_code: int = None, response_text: str = None, url: str = None):
        self.status_code = status_code
        self.response_text = response_text
        self.url = url
        super().__init__(f"{message} (Status code: {status_code}, URL: {url})\nResponse: {response_text}")


class IcometrixParseException(IcometrixException):
    fmt = "Failed to parse HTTP response body"


class IcometrixConfigException(IcometrixException):
    fmt = "Invalid configuration"


class IcometrixAuthException(IcometrixException):
    fmt = "Authentication failed"


class IcometrixDataImportException(IcometrixException):
    fmt = "Dicom import failed"


class IcometrixInvalidInputDataException(IcometrixException):
    fmt = "Data validation failed"


class WaitTimeoutException(IcometrixException):
    ...


class IcometrixUnusableReportException(IcometrixException):
    pass
