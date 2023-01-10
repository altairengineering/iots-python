import json

from requests import Response


def make_json_response(status_code: int, body=None) -> Response:
    resp = Response()
    resp.status_code = status_code
    resp._content = json.dumps(body).encode('utf-8')
    return resp
