# SmartWorks API Client <!-- NODOC -->

**A Python client for the SmartWorks API** <!-- NODOC -->

## Introduction

This library allows you to interact with the SmartWorks API using Python.
The current implementation has support for:
- Categories API <b>(only <code>GET</code> methods)</b>
- Things API <b>(only <code>GET</code> methods)</b>
- Properties API
- Actions API
- Events API

## Install

From PyPI:

```shell
$ pip install swx
```

This library officially supports Python 3.7+.

## The API class

All the requests are made using an instance of the `API` class. There are
multiple ways to deal with authentication:

- Setting a token at instantiation time:
  
  ```python
  from swx import API
  
  my_token = "some-access-token"
  api = API(host="api.swx.altairone.com", token=my_token)
  ```

- Setting a token after instantiation:
  
  ```python
  api = API(host="api.swx.altairone.com")
  api.set_token(my_token)
  ```

- Using an OAuth2 client credentials with manual token revocation:
  
  ```python
  my_client_id = "some-client-id"
  my_client_secret = "the-client-secret"
  my_scopes = ["category", "thing"]
  api = API(host="api.swx.altairone.com").credentials(my_client_id, my_client_secret, my_scopes)
  
  # ...
  
  api.revoke_token()
  ```

- Using an OAuth2 client credentials with automatic token revocation:
  
  ```python
  with API(host="api.swx.altairone.com").credentials(my_client_id, my_client_secret, my_scopes) as api:
      # ...
      # The token will be revoked when the 'with' block ends
      # or if the function returns or raises an exception
  ```

## Using the API

The `API` class uses a nested syntax to allow accessing the API resources,
setting the request information with the same structure order that the one used
by the API endpoints. Some examples:

```python
# List Categories
categories = api.categories().get()

# Get a specific Thing
thing = api.things("01GQ2E9M2Y45BX9EW0F2BM032Q").get()

# List Things inside a Category
things = api.categories("Sensors").things().get()

# Get all the Property values of a Thing
properties = api.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties().get()

# Get a specific Property value
property = api.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").get()

# Set a Property value
property = api.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").update(17.3)

# Create a new Action value
action = api.things("01GQ2E9M2Y45BX9EW0F2BM032Q").actions("updateFirmware").create({"updateFirmware": {"input": "v2.0.0"}})
```

The models used by the API for request and response data can be found in the
`swx.models` package.

> **Note:** The API resources use type hints that should help to understand
> how to use the API and the data models to define input data or
> access response data.

## 🔮 Future features
- Iterate pagination results.
- List filters.
- Auto-refresh access token.
- Support create, update and delete methods in Categories and Things APIs.
- Add more API resource components.
