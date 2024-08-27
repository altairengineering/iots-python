# import json
# from datetime import datetime
# from unittest import mock
#
# import pytest
# from pydantic import BaseModel
#
# from iots.api import API
# from iots.models.models import PropertyHistoryValueList, Properties, PropertyHistoryValue, \
#     CreatePropertyHistoryValuesRequest, PropertyHistoryValues
# from .common import make_response, to_json
# from .test_api_pagination import assert_pagination
#
# request_mock_pkg = 'iots.api.requests.request'
#
# test_properties_history_value_payload = {
#     "at": "2024-04-02T11:17:09.122Z",
#     "properties": {
#         "humidity": 10
#     }
# }
#
# test_properties_history_values = [
#     {
#         "at": "2024-04-02T11:17:09.122Z",
#         "properties": {
#             "humidity": 10
#         }
#     },
#     {
#         "at": "2024-04-02T11:17:09.122Z",
#         "properties": {
#             "is_raining": True
#         }
#     },
#     {
#         "at": "2024-04-02T11:17:04.703Z",
#         "properties": {
#             "is_raining": False
#         }
#     },
#     {
#         "at": "2024-04-02T11:17:02.518Z",
#         "properties": {
#             "temperature": 21
#         }
#     },
#     {
#         "at": "2024-04-02T11:16:58.157Z",
#         "properties": {
#             "humidity": 7
#         }
#     },
#     {
#         "at": "2024-04-02T11:16:56.417Z",
#         "properties": {
#             "humidity": 1
#         }
#     },
#     {
#         "at": "2024-04-02T11:16:52.499Z",
#         "properties": {
#             "humidity": 0
#         }
#     }
# ]
#
#
# def compare_properties_history_value(a, b):
#     class DateTimeModel(BaseModel):
#         dt: datetime
#
#     dt_a = a['at']
#     if not isinstance(dt_a, datetime):
#         dt_a = DateTimeModel(dt=dt_a).dt
#
#     dt_b = b['at']
#     if not isinstance(dt_b, datetime):
#         dt_b = DateTimeModel(dt=dt_b).dt
#
#     assert dt_a == dt_b
#     assert a['properties'] == b['properties']
#
#
# @pytest.mark.parametrize("req_payload", [
#     CreatePropertyHistoryValuesRequest.parse_obj(test_properties_history_value_payload),
#     test_properties_history_value_payload,
# ])
# def test_create(req_payload):
#     """
#     Tests a successful request to create a Properties-history value.
#     """
#     expected_resp_payload = test_properties_history_value_payload
#
#     expected_resp = make_response(201, expected_resp_payload)
#
#     with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
#         action = (API(host="test-api.swx.altairone.com").
#                   set_token("valid-token").
#                   spaces("space01").
#                   things("thing01").
#                   properties_history().
#                   create(req_payload, params={'foo': 'bar'}))
#
#     m.assert_called_once_with("POST",
#                               "https://test-api.swx.altairone.com/spaces/space01/things",
#                               params={'foo': 'bar'},
#                               headers={
#                                   'Authorization': 'Bearer valid-token',
#                                   'Content-Type': 'application/json',
#                               },
#                               data=to_json(req_payload),
#                               timeout=3)
#
#     assert action == PropertyHistoryValues.parse_obj(expected_resp_payload)
#     assert isinstance(action, PropertyHistoryValues)
#
#
# def test_list():
#     """
#     Tests a successful request to get the properties-history values of all the
#     Properties of a Thing.
#     """
#     expected_resp_payload = {
#         "data": test_properties_history_values,
#         "paging": {
#             "next_cursor": "",
#             "previous_cursor": ""
#         }
#     }
#
#     expected_resp = make_response(200, expected_resp_payload)
#
#     with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
#         values = (API(host="test-api.swx.altairone.com").
#                   set_token("valid-token").
#                   spaces("space01").
#                   things("thing01").
#                   properties_history().
#                   get(params={'foo': 'bar'}))
#
#     m.assert_called_once_with("GET",
#                               "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties-history",
#                               params={'foo': 'bar'},
#                               headers={'Authorization': 'Bearer valid-token'},
#                               data=[],
#                               timeout=3)
#
#     for i, v in enumerate(values):
#         compare_properties_history_value(v, expected_resp_payload['data'][i])
#
#     assert values == PropertyHistoryValueList.parse_obj(expected_resp_payload)
#     assert isinstance(values, PropertyHistoryValueList)
#
#     # Test pagination
#     pagination_function = (API(host="test-api.swx.altairone.com").
#                            set_token("valid-token").
#                            spaces("space01").
#                            things("thing01").
#                            properties_history().
#                            get)
#
#     for limit in range(1, 10):
#         assert_pagination(pagination_function,
#                           "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties-history",
#                           test_properties_history_values, limit, {'foo': 'bar'},
#                           lambda x: str(test_properties_history_values.index(x)), PropertyHistoryValue)
#
#
# def test_list_by_property_name():
#     """
#     Tests a successful request to get the properties-history values of a
#     specific Property.
#     """
#     test_properties_history_humidity_values = [v for v in test_properties_history_values if
#                                                'humidity' in v['properties']]
#
#     expected_resp_payload = {
#         "data": test_properties_history_humidity_values,
#         "paging": {
#             "next_cursor": "",
#             "previous_cursor": ""
#         }
#     }
#
#     expected_resp = make_response(200, expected_resp_payload)
#
#     with mock.patch(request_mock_pkg, return_value=expected_resp) as m:
#         values = (API(host="test-api.swx.altairone.com").
#                   set_token("valid-token").
#                   spaces("space01").
#                   things("thing01").
#                   properties_history("humidity").
#                   get(params={'foo': 'bar'}))
#
#     m.assert_called_once_with("GET",
#                               "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties-history/humidity",
#                               params={'foo': 'bar'},
#                               headers={'Authorization': 'Bearer valid-token'},
#                               data=[],
#                               timeout=3)
#
#     for i, v in enumerate(values):
#         compare_properties_history_value(v, expected_resp_payload['data'][i])
#
#     assert values == PropertyHistoryValueList.parse_obj(expected_resp_payload)
#     assert isinstance(values, PropertyHistoryValueList)
#
#     # Test pagination
#     pagination_function = (API(host="test-api.swx.altairone.com").
#                            set_token("valid-token").
#                            spaces("space01").
#                            things("thing01").
#                            properties_history("humidity").
#                            get)
#
#     for limit in range(1, 10):
#         assert_pagination(pagination_function,
#                           "https://test-api.swx.altairone.com/spaces/space01/things/thing01/properties-history/humidity",
#                           test_properties_history_humidity_values, limit, {'foo': 'bar'},
#                           lambda x: str(test_properties_history_humidity_values.index(x)), PropertyHistoryValue,
#                           lambda x: len(x.properties) == 1 and 'humidity' in x.properties)
