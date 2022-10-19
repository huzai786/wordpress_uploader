"""operational utilities for frontend"""
from typing import Optional

import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth


WP_URL = "http://mylocalsite/wp-json/wp/v2"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
auth = HTTPBasicAuth('user', 'avg6 vSOR 1o5R uVmy z5O1 qSEZ')


def add_category_to_wp(category_name: str) -> Optional[int]:
    """
    Creates category in word press database
    :param category_name: Name of the category to be created in word press
    :return: returns the id if created successfully
    """

    global WP_URL, headers, auth
    data = {
        "name": category_name,
        "slug": category_name,
        "parent": 0
    }
    try:
        res = requests.post(WP_URL + '/categories', auth=auth, headers=headers, json=data)
        if res.status_code == 201:
            return res.json().get('id')
        else:
            return None

    except RequestException as e:
        print(e)


def delete_category_from_wp(category_id):
    """
    Creates category in word press database
    """
    global WP_URL, headers, auth

    try:
        res = requests.delete(WP_URL + f'/categories/{category_id}', auth=auth, headers=headers, json={"force": True})
        if res.status_code == 200:
            deleted = res.json().get('deleted')
            if deleted:
                return True
        else:
            print(res.status_code)
            return False

    except RequestException as e:
        print(e)

def add_keyword_to_wp(parent_id: int) -> int:
    """
    add keyword as sub-category to the word press.

    :param parent_id: category id to which this keyword will belong to.
    :rtype: int: return the newly created sub category.
    """

