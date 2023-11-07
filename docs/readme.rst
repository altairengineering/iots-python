.. role:: raw-html-m2r(raw)
   :format: html


Introduction
------------

This library allows you to interact with the SmartWorks API using Python.
The current implementation has support for:


* Categories API :raw-html-m2r:`<b>(only <code>GET</code> methods)</b>`
* Things API :raw-html-m2r:`<b>(only <code>GET</code> methods)</b>`
* Properties API
* Actions API
* Events API

Install
-------

From PyPI:

.. code-block:: shell

   pip install swx

This library officially supports Python 3.7+.

The API class
-------------

All the requests are made using an instance of the ``API`` class.

.. code-block:: python

   from swx import API

   api = API()

By default, the API class will use the host ``https://api.swx.altairone.com``.
You can also specify a different host:

.. code-block:: python

   from swx import API

   api = API(host="https://api.my-smartworks.com")

Authentication
^^^^^^^^^^^^^^

There are multiple ways to deal with authentication:


* 
  Setting a token at instantiation time:

  .. code-block:: python

     from swx import API

     my_token = "some-access-token"
     api = API(host="api.swx.altairone.com", token=my_token)

* 
  Setting a token after instantiation:

  .. code-block:: python

     api = API(host="api.swx.altairone.com")
     api.set_token(my_token)

* 
  Using an OAuth2 client credentials with manual token revocation:

  .. code-block:: python

     my_client_id = "some-client-id"
     my_client_secret = "the-client-secret"
     my_scopes = ["category", "thing"]
     api = API(host="api.swx.altairone.com").get_token(my_client_id, my_client_secret, my_scopes)

     # ...

     api.revoke_token()

* 
  Using an OAuth2 client credentials with automatic token revocation:

  .. code-block:: python

     with API(host="api.swx.altairone.com").get_token(my_client_id, my_client_secret, my_scopes) as api:
         # ...
         # The token will be revoked when the 'with' block ends
         # or if the function returns or raises an exception

..

   ⚠️ **Note:** Tokens are not automatically refreshed (yet). If a token expires,
   you'll need to request a new one.


Using the API
-------------

The ``API`` class uses a nested syntax to allow accessing the API resources,
setting the request information with the same structure order that the one used
by the API endpoints. Some examples:

.. code-block:: python

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
   properties = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties().get()

   # Get a specific Property value
   property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").get()

   # Set a Property value
   property = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").properties("temperature").update(17.3)

   # Create a new Action value
   action = space.things("01GQ2E9M2Y45BX9EW0F2BM032Q").actions("updateFirmware").create({"updateFirmware": {"input": "v2.0.0"}})

The models used by the API for request and response data can be found in the
``swx.models`` package.

..

   💡 **Note:** The API resources use type hints that should help to understand
   how to use the API and the data models to define input data or access
   response data.


Query parameters
^^^^^^^^^^^^^^^^

To add any query parameter to a request, use the ``param`` argument with a
dictionary of parameters:

.. code-block:: python

   # Return up to 100 Things that have a "temperature" Property with value >= 20
   things = space.things().get(params={
     'property:temperature': 'gte:20',
     'limit': 100,
   })

Pagination
^^^^^^^^^^

Some resource listing operations support pagination. You can iterate the
response instances to retrieve all the results. If additional API calls are
needed to fetch the remaining results, they will be made behind the scenes.

.. code-block:: python

   # Get all the Things in a Space
   things = space.things().get()

   for t in things:
       print(t.uid)

🔮 Future features
------------------


* Auto-refresh access token.
* Support create, update and delete methods in Categories and Things APIs.
* Add more API resource components.
