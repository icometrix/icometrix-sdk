from urllib3 import encode_multipart_formdata


def create_multipart(fields, boundary=None):
    """
    Wrapper around urllib3 "encode_multipart_formdata"

    :param fields:
        Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).

    :param boundary:
        If not specified, then a random boundary will be generated using
        :func:`urllib3.filepost.choose_boundary`.
    """
    data, content_type = encode_multipart_formdata(fields, boundary)
    headers = {"Content-Type": content_type, 'Content-Length': str(len(data))}
    return data, headers
