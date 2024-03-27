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

This library officially supports Python 3.7+.

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

api = API(host="https://api.my-smartworks.com")
```

### Authentication

There are multiple ways to deal with authentication:

- Setting an already-exchanged access token:
  
  ```python
  api = API(host="api.swx.altairone.com").set_token("my-access-token")
  ```

- Using an OAuth2 client credentials with manual token revocation:
  
  ```python
  my_client_id = "some-client-id"
  my_client_secret = "the-client-secret"
  my_scopes = ["category", "thing"]
  api = API(host="api.swx.altairone.com").set_credentials(my_client_id, my_client_secret, my_scopes)
  
  # ...
  
  api.revoke_token()
  ```

- Using an OAuth2 client credentials with automatic token revocation:
  
  ```python
  with API(host="api.swx.altairone.com").set_credentials(my_client_id, my_client_secret, my_scopes) as api:
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
space = api.spaces("my-iot-project")

# List Categories
categories = space.categories().get()

# Get a specific Thing
thing = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").get()

# List Things inside a Category
things = space.categories("Sensors").things().get()

# List Things with query parameters
things = space.things().get(params={"property:temperature": "gt:20"})

# Get all the Property values of a Thing
thing_properties = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties().get()
# ... and access to the 'temperature' Property
temperature = thing_properties['temperature']

# Get a specific Property value
thing_property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").get()
temperature = thing_properties['temperature']

# Set a Property value
thing_property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").update(17.3)

# Create a new Action value
action = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").actions("updateFirmware").create({"updateFirmware": {"input": "v2.0.0"}})
```

The models used by the API for request and response data can be found in the
`iots.models.models` module.

> 💡 **Note:** The API resources use type hints that should help to understand
> how to use the API and the data models to define input data or access
> response data.

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

## 🔮 Future features
- Add more API resource components.
- Support for asynchronous requests.
