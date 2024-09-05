from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pyexpat import ExpatError
from typing import Tuple, Union

import requests
from requests import HTTPError, PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

from ..models.basemodel import APIBaseModel
from ..models.exceptions import ExceptionList, ResponseError
from ..models.extensions.pagination import PaginationDescription
from .content_type import (
    SUPPORTED_REQUEST_CONTENT_TYPES,
    content_types_compatible,
    content_types_match,
)
from .runtime_expr import evaluate, prepare_request


def _is_api(obj):
    from ..api import API
    return isinstance(obj, API)


@dataclass
class APIResource(ABC):
    """
    Abstract class to represent a part of an API call.
    This must be inherited by any class implementing an API operation.
    """

    _stack: list = field(default_factory=list, init=False)
    """
    A list used to store the objects generated during a call chain.
    This allows to access all the information needed to make an API request,
    such as building the request URL.

    Items in the stack can be:
    - One (and only one) `API` instance. This must be the first item in the
      stack.
    - A number of `APIResource` building the request.
    """

    @abstractmethod
    def _build_partial_path(self):
        pass

    def _with_stack(self, stack: list):
        self._stack = stack
        return self

    def _child_of(self, obj):
        """
        Sets the stack of this instance to a copy of the given `APIResource`
        stack with the object itself added.
        This method is used when a new `APIResource` instance is created from
        another one.
        """
        if _is_api(obj):
            self._stack = [obj]
        else:
            self._stack = obj._stack.copy()
            self._stack.append(obj)
        return self

    def _build_url(self) -> str:
        """
        Builds and returns the URL using all the stack information.
        The first item in the stack must be an `API` instance, and the rest
        must be `APIResource` instances.
        """
        if len(self._stack) == 0 or not _is_api(self._stack[0]):
            raise RuntimeError("API instance is missing in the stack")

        return self._stack[0].host.rstrip("/") + self._build_path()

    def _build_path(self) -> str:
        """
        Builds the URL path using all the `APIResource` instances in the stack.
        """
        path = ""
        for obj in self._stack:
            if isinstance(obj, APIResource):
                path = path + obj._build_partial_path()

        return path + self._build_partial_path()

    def _path_value(self, path_param_name: str):
        """
        Returns the value of the given path parameter.
        """
        if hasattr(self, path_param_name):
            return getattr(self, path_param_name)

        for r in self._stack[1:]:
            if hasattr(r, path_param_name):
                return getattr(r, path_param_name)

        return None

    def _path_values(self) -> dict:
        """
        Returns a dictionary with the values of all the path parameters of the
        current stack.
        """
        values = {k: v for k, v in self.__dict__.items() if k != '_stack'}
        for r in self._stack[1:]:
            values.update({k: v for k, v in r.__dict__.items() if k != '_stack'})

        return values

    def _api(self):
        if len(self._stack) == 0 or not _is_api(self._stack[0]):
            raise RuntimeError("API instance is missing in the stack")
        return self._stack[0]

    def _make_request(self, method="GET", body=None, req_content_types: list = None, **kwargs) -> Response:
        api = self._api()

        body, headers = _validate_request_payload(body, req_content_types, kwargs.get('headers'))
        kwargs['headers'] = headers

        return api.make_request(method, self._build_path(), body=body, **kwargs)

    def _handle_response(self, response: requests.Response, expected_responses: list,
                         param_types: dict = None,
                         pagination_info: PaginationDescription = None):
        default_status_code = 0

        # Send default expected response to the end of the list
        expected_responses = sorted(expected_responses, key=lambda x: x[0] == 0)

        expected_status_codes = set([r[0] for r in expected_responses])
        if (response.status_code not in expected_status_codes
                and default_status_code not in expected_status_codes):
            raise ResponseError(response, f"Unexpected response status code ({response.status_code})")

        resp_content_type = response.headers.get('content-type')
        for r in expected_responses:
            code, content_type, resp_class = r

            if not content_type:
                ret = resp_class()

                ret._set_http_response(response)
                self._handle_pagination(ret, response, pagination_info,
                                        self._path_values(), param_types,
                                        expected_responses)

                return self._handle_error(ret)

            if (code in [response.status_code, default_status_code]
                    and content_types_match(resp_content_type, content_type)):
                resp_payload = response.content
                if resp_content_type.startswith('application/json'):
                    resp_payload = response.json()
                elif resp_content_type.startswith('application/xml'):
                    import xmltodict
                    resp_payload = xmltodict.parse(response.content)['root']
                elif resp_content_type.startswith('text/plain'):
                    resp_payload = resp_payload.decode('utf-8')

                ret = resp_class.parse_obj(resp_payload)

                ret._set_http_response(response)
                self._handle_pagination(ret, response, pagination_info,
                                        self._path_values(), param_types,
                                        expected_responses)

                return self._handle_error(ret)

        raise ResponseError(response, f"Unexpected response content type ({resp_content_type})")

    def _handle_error(self, ret):
        api = self._stack[0]
        if api._raise_errors:
            try:
                ret.http_response().raise_for_status()
            except HTTPError as e:
                raise ResponseError(ret, str(e))

        return ret

    def _handle_pagination(self, ret: APIBaseModel, resp: Response,
                           pagination_info: PaginationDescription,
                           path_values: dict, params_info: dict,
                           expected_responses: list):
        """
        Add metadata to the returned model object to allow handling pagination.
        """
        if pagination_info is None:
            return None

        if params_info is None:
            params_info = {}

        ret._enable_pagination(pagination_info.result)
        ret._pagination.iter_func = None

        query_params = params_info.get('query')
        headers = params_info.get('header')

        has_more = evaluate(resp, pagination_info.has_more, path_values,
                            query_params, headers)
        if not has_more:
            return

        req = PreparedRequest()
        if pagination_info.reuse_previous_request:
            req = resp.request
        if pagination_info.url:
            url = evaluate(resp, pagination_info.url, path_values, query_params, headers)
            req.prepare_url(url, None)
        if pagination_info.method:
            # TODO: Evaluate expression ???
            req.prepare_method(pagination_info.method)
        for modifier in pagination_info.modifiers:
            # TODO: Evaluate complex expressions
            value = evaluate(resp, modifier.value, path_values, query_params, headers)
            prepare_request(req, modifier.param, value)

        def make_request():
            api = self._api()
            new_resp = api.make_request(req.method, req.url, req.body,
                                        headers=req.headers)
            return self._handle_response(new_resp, expected_responses, params_info, pagination_info)

        ret._pagination.iter_func = make_request


def _validate_request_payload(body: Union[str, bytes, dict, APIBaseModel],
                              req_content_types: list, headers: dict) -> Tuple[str, dict]:
    """
    Tries to parse the request body into one of the supported pairs of
    content-type / class type. An exception will be returned if the body
    doesn't match any of the given expected types.

    If req_content_types is None or an empty list, this is a no-op.

    :param body:              Payload of the request.
    :param req_content_types: List of tuples defining the supported types of the
                              request. The first element of each tuple is the
                              Content-Type, and the second one is the class of
                              the payload model.
    :param headers:           The headers of the request. If a Content-Type is
                              set, only the types in req_content_types that
                              matches that Content-Type will be validated.
    :return:                  The body ready to be sent, and the headers with
                              the proper Content-Type added.
    """
    exceptions_raised = []

    if req_content_types:
        content_type_defined = False

        # If Content-Type header is set, only that one is allowed
        headers = CaseInsensitiveDict(headers)
        headers.items()
        expected_content_type = headers.get('content-type', None)
        if expected_content_type:
            content_type_defined = True
            req_content_types = [(content_type, req_class) for content_type, req_class in req_content_types if
                                 content_types_match(content_type, expected_content_type)]

        for content_type, request_class in req_content_types:
            # TODO: currently, request_class is not used, but it could be used
            #       to validate that the payload matches a given model
            for ct, conv_func in SUPPORTED_REQUEST_CONTENT_TYPES.items():
                if content_types_compatible(content_type, ct):
                    try:
                        body = conv_func(body)

                        if not content_type_defined:
                            # Set content type header
                            headers['Content-Type'] = content_type
                        return body, dict(headers)
                    except (ValueError, ExpatError) as e:
                        exceptions_raised.append(e)

    if len(exceptions_raised) > 0:
        raise ExceptionList('Unexpected data format', exceptions_raised)

    return body, headers
