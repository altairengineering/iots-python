import json
import re
from functools import reduce
from typing import Union
from urllib.parse import parse_qs, urlparse

from requests import PreparedRequest, Request, Response


class RuntimeExpressionError(Exception):
    """ Invalid runtime expression. """

    def __init__(self, *attrs, caused_by: Exception = None):
        super().__init__(*attrs)
        self.caused_by = caused_by


def evaluate(resp: Union[dict, Response], expression: str, path_values: dict = None,
             query_param_types: dict = None, header_param_types: dict = None):
    """
    Evaluates an OpenAPI runtime expression (https://swagger.io/docs/specification/links/).
    It also accepts a dot-separated expression to address an attribute of the
    response body.

    It raises a RuntimeExpressionError if the expression cannot be evaluated
    successfully.

    :param resp:        The response on which the expression will be applied.
    :param expression:  An OpenAPI runtime expression or a dot-separated expression.
    :param path_values: A dictionary with the values of the path parameters of
                        the request. It is only needed if the runtime expression
                        needs to access these values.
    :param query_param_types: A dictionary with the types of the query parameters of
                        the request. It is only needed if the values have to be
                        returned with the appropriate type. Otherwise, a string value
                        will be returned.
    :param header_param_types: A dictionary with the types of the header parameters of
                        the request. It is only needed if the values have to be
                        returned with the appropriate type. Otherwise, a string value
                        will be returned.
    :return:            The result of the evaluated expression.
    """
    try:
        expression = expression.strip()

        if '{' in expression:
            def replace_group(match):
                return str(_evaluate_runtime_expression(resp, match.group(1),
                                                        path_values=path_values,
                                                        query_param_types=query_param_types,
                                                        header_param_types=header_param_types))

            return re.sub(r'{(\$[^}]+)}', replace_group, expression)

        if expression.startswith('$'):
            return _evaluate_runtime_expression(resp, expression,
                                                path_values=path_values,
                                                query_param_types=query_param_types,
                                                header_param_types=header_param_types)

        if isinstance(resp, Response):
            resp = resp.json()

        if not isinstance(resp, dict):
            raise ValueError("Invalid dict response")

        return _get_from_dict(resp, expression)
    except RuntimeExpressionError as e:
        raise e
    except Exception as e:
        raise RuntimeExpressionError(caused_by=e)


def _evaluate_runtime_expression(resp: Response, expression: str,
                                 path_values: dict = None,
                                 query_param_types: dict = None,
                                 header_param_types: dict = None):
    """
    Decodes the given runtime expression (according to
    https://swagger.io/docs/specification/links/) and returns the evaluated value.
    """
    if header_param_types is not None:
        header_param_types = {k.lower(): v for k, v in header_param_types.items()}

    def to_string(obj):
        return str(obj) if obj is not None else ''

    def cast_value(name, value, type_dict):
        if type_dict is not None and name in type_dict:
            return type_dict[name](value)
        return value

    def get_query_string(name):
        parsed_url = urlparse(resp.request.url)
        query_params = parse_qs(parsed_url.query)
        value = query_params.get(name, [])
        if len(value) == 0:
            raise RuntimeExpressionError(f"Query parameter '{name}' not found")
        elif len(value) == 1:
            return value[0]
        else:
            return value

    def get_path_value(name):
        if path_values is not None and name in path_values:
            return path_values[name]
        raise RuntimeExpressionError(f"Path parameter '{name}' not found")

    expression_funcs = {
        '$url': lambda: resp.request.url,
        '$method': lambda: resp.request.method,
        '$request.query.*': lambda x: cast_value(x, get_query_string(x), query_param_types),
        '$request.path.*': lambda x: get_path_value(x),
        '$request.header.*': lambda x: cast_value(x, resp.request.headers.get(x), header_param_types),
        '$request.body': lambda: to_string(resp.request.body),
        '$request.body#/*': lambda x: _get_from_dict(json.loads(resp.request.body), x, '/'),
        '$statusCode': lambda: resp.status_code,
        '$response.header.*': lambda x: resp.headers.get(x),
        '$response.body': lambda: resp.text,
        '$response.body#/*': lambda x: _get_from_dict(resp.json(), x, '/'),
    }

    for expr, fn in expression_funcs.items():
        if expr.endswith('*'):
            expr_prefix = expr.rstrip('*')
            if expression.startswith(expr_prefix):
                return fn(expression[len(expr_prefix):])
        if expr == expression:
            return fn()

    raise RuntimeExpressionError("invalid runtime expression")


def prepare_request(req: Union[PreparedRequest, Request], expression: str, value):
    """
    Set the value of a request from an OpenAPI runtime expression
    (https://swagger.io/docs/specification/links/).
    The expression can also be a dot-separated expression to address an
    attribute of the response body.

    It raises a RuntimeExpressionError if the expression cannot be evaluated
    successfully.

    :param req:         Request to update.
    :param expression:  An OpenAPI runtime expression or a dot-separated expression.
                        Only expressions that can be applied to a request are allowed.
    :param value:       The value to set in the request.
    """
    try:
        expression = expression.strip()

        if isinstance(req, Request):
            req = req.prepare()
        elif not isinstance(req, PreparedRequest):
            raise ValueError(f"Unexpected type '{type(req)}'")

        if expression.startswith('$'):
            _set_expression_value(req, expression, value)
            return req

        if expression:
            if req.body:
                body = json.loads(req.body)
            else:
                body = {}

            _set_in_dict(body, expression, value)
        else:
            body = value

        req.prepare_body(None, None, json=body)
        return req

    except RuntimeExpressionError as e:
        raise e
    except Exception as e:
        raise RuntimeExpressionError(caused_by=e)


def _set_expression_value(req: PreparedRequest, expression: str, value):
    """
    Decodes the given runtime expression (according to
    https://swagger.io/docs/specification/links/) and applies the given value
    to the corresponding field.
    """

    def set_query_param(name):
        parsed_url = urlparse(req.url)
        query_params = parse_qs(parsed_url.query)
        query_params[name] = value
        parsed_url = parsed_url._replace(query=None)
        req.prepare_url(parsed_url.geturl(), query_params)

    expression_funcs = {
        '$url': lambda: req.prepare_url(value, None),
        '$method': lambda: req.prepare_method(value),
        '$request.query.*': lambda x: set_query_param(x),
        '$request.header.*': lambda x: req.headers.__setitem__(x, value),
        '$request.body': lambda: req.prepare_body(None, None, value),
        '$request.body#/*': lambda x: req.prepare_body(None, None,
                                                       _set_in_dict(json.loads(req.body or '{}'),
                                                                    x, value, '/')),
    }

    for expr, fn in expression_funcs.items():
        if expr.endswith('*'):
            expr_prefix = expr.rstrip('*')
            if expression.startswith(expr_prefix):
                return fn(expression[len(expr_prefix):])
        if expr == expression:
            return fn()

    raise RuntimeExpressionError("invalid runtime expression")


def _get_from_dict(d: dict, key: str, separator='.'):
    try:
        def get_item(a, b):
            if isinstance(a, list):
                b = int(b)
            return a[b]

        return reduce(get_item, key.split(separator), d)
    except KeyError:
        raise KeyError(f"Key '{key}' not found")
    except IndexError:
        raise IndexError(f"Index '{key}' out of range")


def _set_in_dict(d: dict, key: str, value, separator='.'):
    temp_dict = d

    def get_next(obj: Union[dict, list], subkey: str, set_value: bool = False):
        default_value = value if set_value else {}

        if isinstance(obj, dict):
            next_level = obj.setdefault(subkey, default_value)
        elif isinstance(obj, list):
            if subkey == '-':
                obj.append(default_value)
                return obj[-1]
            subkey = int(subkey)
            next_level = obj[subkey]
        else:
            raise ValueError(f"Unexpected type '{type(obj)}'. Expected 'dict' or 'list'")

        if not set_value and not isinstance(next_level, (dict, list)):
            obj[subkey] = {}
            return obj[subkey]

        if set_value:
            obj[subkey] = value
            return obj[subkey]

        return next_level

    *key, last = key.strip().split(separator)
    for bit in key:
        temp_dict = get_next(temp_dict, bit)
    get_next(temp_dict, last, True)
    return d
