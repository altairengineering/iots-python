import json

import requests

from urllib.parse import urljoin
from swx.auth.token import Token
from swx.errors import ResponseError


class Category:  # class to work with Categories

    """
    :param token:         Token obtained from the oauth package with the function "get_token".
    :param space_name:    Name of the space we want to work on.
    :param category_name: Name of the category we want to work on.
    If we want to work over all the Categories this parameter must be empty.
    """

    def __init__(self, token: Token, space_name: str, category_name=""):
        self.token = token
        self.space = space_name
        self.category = category_name


class Things:  # class to work with Things

    """
    :param token:         Token obtained from the oauth package with the function "get_token".
    :param space_name:    Name of the space we want to work on.
    :param category_name: Name of the category we want to work on.
    If we do not want to work on one, the parameter must be an empty string.
    :param thing_id:      UID of the Thing that we want to work with.
    If we want to work over all the Things this parameter must be empty.
    """

    def __init__(self, token: Token, space_name: str, category_name: str, thing_id=""):
        self.token = token
        self.space = space_name
        self.category = category_name
        self.id = thing_id
        self.value = None

    def get(self):
        url = generate_thing_url(self.token, self.space, self.category, self.id)
        return get_info(url, self.token)

    def create(self, value):
        pass

    def update(self, value):
        pass

    def delete(self):
        pass


class Properties:

    """
    :param thing:         Thing on which we are going to work on properties obtained from Thing class.
    :param property_name: Name of the Property that we want to work over.
    If we want to work over all the Properties of a Thing this parameter must be empty.
    """

    def __init__(self, thing: Things, property_name=""):
        self.value = None
        self.property_name = property_name
        self.thing = thing

    def get(self):
        if self.thing.id == "":
            e = ResponseError(400, "Cannot recover Properties info, ThingID is missing")
            print(e)
            return e
        url = generate_properties_url(self.thing.token, self.thing.space, self.thing.category, self.thing.id,
                                      self.property_name)
        return get_info(url, self.thing.token)

    def update(self, value):
        if self.thing.id == "":
            e = ResponseError(400, "Cannot update Properties, ThingID is missing")
            print(e)
            return e
        url = generate_properties_url(self.thing.token, self.thing.space, self.thing.category, self.thing.id,
                                      self.property_name)
        if self.property_name == "":
            return post_info(url, self.thing.token, value)
        else:
            json_value = {self.property_name: value}
            return post_info(url, self.thing.token, json_value)


# the function 'get_info' is used to make GET requests
def get_info(url: str, token):
    r = requests.get(url, headers={"Authorization": token.token_type + " " + token.access_token})
    if r.status_code > 299:
        print(r.text)
    return r.text


# the function 'post_info' is used to make POST requests
def post_info(url: str, token, body):
    r = requests.post(url, json=body, headers={"Content-Type": "application/json;charset=UTF-8",
                                               "Authorization": token.token_type + " " + token.access_token})
    if r.status_code > 299:
        print(r.text)
    return r.json()


# the function 'update_info' is used to make PUT requests
def update_info(url: str, token, body):
    r = requests.put(url, json=body, headers={"Content-Type": "application/json;charset=UTF-8",
                                              "Authorization": token.token_type + " " + token.access_token})
    if r.status_code > 299:
        print(r.text)
    return r.json()


# the function 'delete_info' is used to make DELETE requests
def delete_info(url: str, token):
    r = requests.delete(url, headers={"Authorization": token.token_type + " " + token.access_token})
    if r.status_code > 299:
        print(r.text)
    return r.status_code


def generate_url(token: Token, space: str, category=""):
    url = urljoin(token.host, "/spaces/" + space)
    if category != "":
        url += "/categories/" + category
    return url


def generate_thing_url(token: Token, space: str, category: str, thing_id: str):
    url = generate_url(token, space, category)
    url += "/things"
    if thing_id != "":
        url += "/" + thing_id
    return url


def generate_properties_url(token: Token, space: str, category: str, thing_id: str, property_name: str):
    url = generate_thing_url(token, space, category, thing_id)
    url += "/properties"
    if property_name != "":
        url += "/" + property_name
    return url
