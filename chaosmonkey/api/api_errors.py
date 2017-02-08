"""
This module contains an object that represent an API Error

Any APIError thrown in an endpoint is handled to return to the user
a proper json error with custom status code and message
"""


class APIError(Exception):
    """
    Represents an API Error

    :param message: message to be returned to the user
    :param status_code: response status code (defaults to 400)
    :param payload: custom payload to give extra info in the response

    Example:
            >>> raise APIError("Error detected", 500, {"extra": "extra_info"})

    """

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 400
        self.payload = payload

    def to_dict(self):
        """Convert exception to dict"""
        dict_ = dict(self.payload or ())
        dict_['msg'] = self.message
        return dict_

    def __str__(self):
        return '[%d] %s' % (self.status_code, self.message)
