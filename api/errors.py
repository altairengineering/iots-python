class APIException(Exception):
    """
    This exception defines a generic error occurred in the API SDK.
    """


ExcMissingToken = APIException("Access token is not set")
