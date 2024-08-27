import copy
import json
import math
from unittest import mock

import httpretty
import requests

request_mock_pkg = 'iots.api.requests.request'


@httpretty.activate
def assert_pagination(pagination_function: callable, expected_url: str,
                      expected_results: list, limit: int,
                      extra_query_params: dict, get_cursor_func: callable,
                      expected_type, assert_func: callable = None,
                      expected_verify: bool = True):
    """
    Asserts that, given API function (pagination_function) that supports
    pagination, it can be paginated properly.
    """

    def request_callback(request: httpretty.core.HTTPrettyRequest, uri, response_headers):
        # Assert expected query params
        for q in request.querystring:
            if q in ['limit', 'next_cursor', 'previous_cursor']:
                continue
            assert q in extra_query_params
            assert extra_query_params[q] in request.querystring[q]

        limit_resp = int(request.querystring.get('limit', [50])[0])

        data = []
        next_cursor, prev_cursor = '', ''
        next_index, prev_index = len(expected_results), -1

        next_cursor_param = request.querystring.get('next_cursor', None)
        if next_cursor_param:
            next_cursor_param = next_cursor_param[0]
            for i, item in enumerate(expected_results):
                if get_cursor_func(item) >= next_cursor_param:
                    data = expected_results[i:i + limit_resp]
                    next_index = i + limit_resp
                    prev_index = i - 1
                    break
        else:
            data = expected_results[:limit_resp]
            next_index = limit_resp
            prev_index = -1

        if next_index < len(expected_results):
            next_cursor = get_cursor_func(expected_results[next_index])
        if prev_index >= 0:
            prev_cursor = get_cursor_func(expected_results[prev_index])

        resp = {
            "paging": {
                "next_cursor": next_cursor,
                "previous_cursor": prev_cursor
            },
            "data": data
        }

        response_headers["Content-Type"] = "application/json"

        return [200, response_headers, json.dumps(resp)]

    httpretty.register_uri(httpretty.GET, expected_url, body=request_callback)
    query_params = copy.deepcopy(extra_query_params)
    query_params['limit'] = limit

    original_request_func = requests.request

    def side_effect(*args, **kwargs):
        # Makes a real call to the request function
        response = original_request_func(*args, **kwargs)
        assert 'verify' in kwargs and kwargs['verify'] == expected_verify
        return response

    with mock.patch(request_mock_pkg) as m:
        m.side_effect = side_effect

        actual_result = pagination_function(params=query_params)

        assert len(httpretty.latest_requests()) == 1
        if limit < len(expected_results):
            assert len(actual_result.data) == limit
        else:
            assert len(actual_result.data) == len(expected_results)

        # Iterate results
        for result_index, result in enumerate(actual_result):
            assert result == expected_type.parse_obj(expected_results[result_index])
            if assert_func:
                assert assert_func(result)

        # Assert that the API has been called until all data has been fetched
        expected_call_count = math.ceil(len(expected_results) / limit)
        assert len(httpretty.latest_requests()) == expected_call_count
        assert m.call_count == expected_call_count
