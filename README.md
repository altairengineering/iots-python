# anythingdbfunctions

How to use "anythingdbfunctions"

First of all we need a token from the function **get_token** defined in the **swx/auth/token.py** file.
It contains the following parameters:

- **host**:            Host URL. **(required)**
- **client_id**:       Client ID. **(required)**
- **client_secret**:   Client Secret. **(required)**
- **scopes**:          List of scopes to request.**(required)**

```Python
import swx.auth.token as auth

token = auth.get_token("<host_url>", "<my_client_id>", "<my_client_secret>", ["<scope_1>", "<scope_2>", "<scope_3>"])
```

Once we have obtained the token we can use the different functions defined in the **swx/functions.py** file.

## Things
Things class contains the following parameters:

- **token**:         Token obtained from the oauth package with the function "get_token". **(required)**
- **space_name**:    Name of the space we want to work on. **(required)**
- **category_name**: Name of the category we want to work on.
If we aren't working over a Category, the parameter must be an empty string. **(required)**
- **thing_id**:      UID of the Thing that we want to work with.
If we want to work over all the Things this parameter must be empty. **(optional)**


```Python
import swx.auth.token as auth
import swx.functions as api

token = auth.get_token("<host_url>", "<my_client_id>", "<my_client_secret>", ["<scope_1>", "<scope_2>", "<scope_3>"])

# GET a specific Thing from a Category
thing_category = api.Things(token,"<space_name>","<category_name>","<thing_id>").get()
# GET all the Things from a Category
things_category = api.Things(token,"<space_name>","<category_name>").get()
# GET a specific Thing regardless of the Category
thing = api.Things(token,"<space_name>","","<thing_id>").get()
# GET all existing Things
things = api.Things(token,"<space_name>","").get()  
```

## Properties
Properties class contains the following parameters:

- **thing**:         Thing on which we are going to work on properties obtained from Thing class. **(required)**
- **property_name**:      Name of the Property that we want to work over.
  If we want to work over all the Properties of a Thing this parameter must be empty. **(optional)**

First of all we need to start a Thing instance, and with that we can work over the Properties of that Thing.
In this case the **thing_id** parameter is necessary.

```Python
import swx.auth.token as auth
import swx.functions as api

token = auth.get_token("<host_url>", "<my_client_id>", "<my_client_secret>", ["<scope_1>", "<scope_2>", "<scope_3>"])
# get the Thing instance. Do not use get() function, because the class is needed, not the information retrieved.
thing = api.Things(token,"<space_name>","","<thing_id>")

# GET the information of the Property given.
property = api.Properties(thing,"<property_name>").get()
# GET the information of the Properties of the Thing
properties = api.Properties(thing).get()

# UPDATE the Property indicated with the value given 
property_updated = api.Things(token,"<space_name>","<property_name>").update(<property_value>)
# UPDATE all the Properties indicated with their respective values 
properties_updated = api.Properties(thing).update({"<property_name_1":<property_value_1>,"<property_name_2":<property_value_2>})
```