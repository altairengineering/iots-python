# Altair IoT Studio API Client <!-- NODOC -->

**A Python client for the Altair® IoT Studio™ API** <!-- NODOC -->

[![pip command](https://img.shields.io/badge/pip_install-iots-orange)](https://pypi.org/project/iots)
[![Supported Versions](https://img.shields.io/pypi/pyversions/iots.svg?logo=python)](https://pypi.org/project/iots)
[![Documentation Status](https://readthedocs.org/projects/iots/badge/?version=latest)](https://iots.readthedocs.io/en/latest/) <!-- NODOC -->

## Introduction

This library allows you to interact with the Altair® IoT Studio™ API using
Python. The current implementation has support for the following AnythingDB
APIs:
- [Categories API](https://openapi.swx.altairone.com/cloud/anything-db#/Categories)
- [Things API](https://openapi.swx.altairone.com/cloud/anything-db#/Things)
- [Properties API](https://openapi.swx.altairone.com/cloud/anything-db#/Properties)
- [Actions API](https://openapi.swx.altairone.com/cloud/anything-db#/Actions)
- [Events API](https://openapi.swx.altairone.com/cloud/anything-db#/Events)

## Install

From PyPI:

```shell
pip install iots
```

This library officially supports Python 3.8+.

## The API class

All the requests are made using an instance of the `API` class.
```python
from iots import API

api = API()
  ```

By default, the API class will use the host `https://api.swx.altairone.com`.
You can also specify a different host:
```python
from iots import API

api = API(host="https://api.my-iot-studio.com")
```

### Authentication

There are multiple ways to deal with authentication:

- Setting an already-exchanged access token:
  
  ```python
  api = API().set_token("my-access-token")
  ```

- Using an OAuth2 client credentials with manual token revocation:
  
  ```python
  my_client_id = "my-client-id"
  my_client_secret = "my-client-secret"
  my_scopes = ["category", "thing"]
  api = API().set_credentials(my_client_id, my_client_secret, my_scopes)
  
  # ...
  
  api.revoke_token()
  ```

- Using an OAuth2 client credentials with automatic token revocation:
  
  ```python
  with API().set_credentials(my_client_id, my_client_secret, my_scopes) as api:
      # ...
      # The token will be revoked when the 'with' block ends
      # or if the code returns or raises an exception
  ```

**Tokens are automatically refreshed** using OAuth2 client credentials, so you
don't need to care about manually refreshing them.

## Using the API

The `API` class uses a nested syntax to allow accessing the API resources,
setting the request information with the same structure order that the one used
by the API endpoints. Some examples:

```python
# Get an instance of a Space that will be used to access resources later.
# Creating this instance will NOT make any request to the API.
space = api.spaces("my-iot-project")

# Get all the Categories in the Space
categories = space.categories().get()

# Get a specific Thing
thing = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").get()

# Get all the Things inside a Category
things = space.categories("Sensors").things().get()

# Get all the Things with some query parameters
things = space.things().get(params={"property:temperature": "gt:20"})

# Get all the Property values of a Thing
thing_properties = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties().get()
# ... and access to the 'temperature' Property
temperature = thing_properties['temperature']

# Get a specific Property value
thing_property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").get()
temperature = thing_properties['temperature']

# Update a Property value
thing_property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").update(17.3)

# Create a new Action value
action = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").actions("updateFirmware").create({"updateFirmware": {"input": "v2.0.0"}})
```

The models used by the API for request and response data can be found in the
`iots.models.models` module.

> 💡 **Note:** The API resources use type hints that should help to understand
> how to use the API and the data models to define input data or access
> response data. It should also help your IDE with code completion and
> displaying documentation.

### Query parameters

To add any query parameter to a request, use the `param` argument with a
dictionary of parameters:

```python
# Return up to 100 Things that have a "temperature" Property with value >= 20
things = space.things().get(params={
  'property:temperature': 'gte:20',
  'limit': 100,
})
```

### Pagination

Some resource listing operations support pagination. You can iterate the
response instances to retrieve all the results. If additional API calls are
needed to fetch the remaining results, they will be made behind the scenes.

```python
# Get all the Things in a Space
things = space.things().get()

for t in things:
    print(t.uid)
```

### Get raw HTTP response

Making an API request returns an instance of an object that represents the
response content. However, you can also access the original response using the
`http_response()` method.

```python
things = api.spaces("my-iot-project").things().get()
# Get the raw response as an instance of requests.Response
raw_response = things.http_response()

status_code = raw_response.status_code
content = raw_response.content
body = raw_response.json()
# ...
```

This method is also available in the raised exceptions, provided that a response
has been returned from the server.

```python
from iots.models.exceptions import ResponseError

try:
    things = api.spaces("my-iot-project").things().get()
except ResponseError as e:
    raw_response = e.http_response()
```

### TLS certificate verification

If you need to skip the TLS certificate verification, you can use the `verify`
argument when creating the `API` instance:

```python
api = API(verify=False)
```


## 🔮 Future features
- Add more API resource components.
- Support for asynchronous requests.
