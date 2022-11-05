"""operational utilities for gui"""
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException

from wp_api.container import PostData


WP_URL = "http://mylocalsite/wp-json/wp/v2"
headers = {"Accept": "application/json", "Content-Type": "application/json"}
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
        res = requests.post(
            WP_URL +
            '/categories',
            auth=auth,
            headers=headers,
            json=data)
        if res.status_code == 201:
            return res.json().get('id')
        else:
            return None

    except RequestException as e:
        print(e)
        return None


def delete_category_from_wp(category_id: int) -> bool:
    """
    Deletes a category in word press database
    :param category_id: category.wp_id to delete
    :return: returns True if successful, else return False
    """
    global WP_URL, headers, auth

    try:
        res = requests.delete(
            WP_URL +
            f'/categories/{category_id}',
            auth=auth,
            headers=headers,
            json={
                "force": True})
        if res.status_code == 200:
            deleted = res.json().get('deleted')
            if deleted:
                return True
        else:
            print(res.status_code)
            return False

    except RequestException as e:
        print(e)
        return False


def add_keyword_to_wp(parent_id: int,
                      keyword_name: str) -> Optional[int]:
    """
    add keyword as sub-category to the word press.

    :param keyword_name: name of the keyword
    :param parent_id: category id to which this keyword will belong to.
    :rtype: int: return the newly created sub category.
    """
    global WP_URL, headers, auth
    data = {
        "name": keyword_name,
        "slug": keyword_name,
        "parent": parent_id
    }
    try:
        res = requests.post(
            WP_URL +
            '/categories',
            auth=auth,
            headers=headers,
            json=data)

        if res.status_code == 201:
            return res.json().get('id')
        else:
            return None

    except RequestException as e:
        print(e)
        return None


def delete_keyword_from_wp(keyword_id):
    """
    Deletes a keyword in word press database

    :param keyword_id: category.wp_id to delete
    :return: returns True if successful, else return False
    """
    global WP_URL, headers, auth

    try:
        res = requests.delete(
            WP_URL +
            f'/categories/{keyword_id}',
            auth=auth,
            headers=headers,
            json={
                "force": True})
        if res.status_code == 200:
            deleted = res.json().get('deleted')
            if deleted:
                return True
        else:
            print(res.status_code)
            return False

    except RequestException as e:
        print(e)
        return False


def delete_post_from_wp(post_id):
    """
    Deletes a post in word press database

    :param post_id: id of the post to delete
    :return: returns True if successful, else return False
    """
    global WP_URL, headers, auth
    try:
        res = requests.delete(
            WP_URL +
            f'/posts/{post_id}',
            auth=auth,
            headers=headers,
            json={
                "force": True})

        if res.status_code == 200:
            deleted = res.json().get('deleted')
            if deleted:
                return True
            else:
                return None

    except RequestException as e:
        print(e)
        return None


def create_post(category_id: int, post_data: PostData) -> Optional[int]:
    """create a post under the provided category.

    :param category_id: sub category/ keyword id
    :param post_data: post data
    :rtype: If successfully created, it will return the newly created post id, else returns None
    """

    global WP_URL, headers, auth
    data = {
        "title": post_data.title,
        "slug": post_data.slug,
        "status": post_data.status,
        "content": post_data.content,
        "excerpt": post_data.excerpt,
        "categories": [category_id]
    }
    try:
        res = requests.post(WP_URL + '/posts', headers=headers, auth=auth, json=data)

        if res.status_code == 201:
            post_id = res.json().get('id')
            return post_id
        else:
            return None

    except RequestException as e:
        print(e)
        return None


