import json


class ResponseError(Exception):
    """
    This exception defines an error response returned by the SmartWorks API.
    """

    def __init__(self, status_code: int, message: str, details: dict = None):
        self.status_code = status_code
        self.message = message
        self.details = details

    def __str__(self):
        return json.dumps(self.json())

    def __repr__(self):
        return f"ResponseError({self.status_code}, {self.message}," \
               f"{self.details})"

    def json(self):
        resp = {
            "error": {
                "status": self.status_code,
                "message": self.message
            }
        }

        if self.details is not None:
            resp["error"]["details"] = self.details

        return resp

    @classmethod
    def parse(cls, resp: dict) -> 'ResponseError':
        if "error" not in resp or not isinstance(resp["error"], dict):
            return cls(0, '')

        return cls(resp["error"].get("status", 0),
                   resp["error"].get("message", ''),
                   resp["error"].get("details", None))


class OAuth2Error(ResponseError):
    """
    This exception defines an error response returned by the OAuth2 server.
    """
    pass


class TokenRevokeError(Exception):
    """
    This exception is thrown when trying to revoke a Token that was not
    obtained successfully.
    """
    pass


class APIException(Exception):
    """
    This exception defines a generic error occurred in the API SDK.
    """


ExcMissingToken = APIException("Access token is not set")
