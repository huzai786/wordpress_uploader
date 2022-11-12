"""operational utilities for gui"""
from typing import Optional, Tuple

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from main import SITE_URL

WP_URL = f"http://{SITE_URL}/wp-json/wp/v2"
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


def add_keyword_to_wp(parent_id: int, keyword_name: str) -> Optional[int]:
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

    res = requests.delete(
            WP_URL +
            f'/posts/{post_id}',
            auth=auth,
            headers=headers,
            json={
                "force": True})

    res.raise_for_status()
    if not res.status_code == 200:
        raise RequestException('request is successful but cant delete')

    return True

def create_post(category_id: str, title: str, excerpt: str, content: str) -> Optional[int]:
    """create a post under the provided category.

    :param excerpt: content excerpt
    :param content: html content
    :param title: title of the post
    :param category_id: sub category/ keyword id

    :rtype: If successfully created, it will return the newly created post id, else returns None
    """

    global WP_URL, headers, auth
    data = {
        "title": title,
        "slug": title,
        "status": 'publish',
        "content": content,
        "excerpt": excerpt,
        "categories": [category_id],
        "format": "image"
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


def upload_image(name: str, image: bytes) -> Optional[Tuple[str, str]]:
    headers = {"Content-Disposition": f'attachment; filename="{name}.jpg"',
               "Accept": "application/json"}
    try:
        res = requests.post(WP_URL + '/media', auth=auth, headers=headers, data=image)
        if i := res.json().get('id'):
            return i, res.json().get('guid').get('raw')

    except RequestException as e:
        print(e)
        return None


def delete_media_from_wp(media_id):
    global WP_URL, headers, auth
    res = requests.delete(WP_URL + f'/media/{media_id}', auth=auth, headers=headers, json={"force": True})
    res.raise_for_status()
    if not res.status_code == 200:
        raise RequestException('request is successful but cant delete')

