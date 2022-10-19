import json

import requests

from requests.auth import HTTPBasicAuth

WP_URL = 'http://mylocalsite/' + "/wp-json/wp/v2"


def get_categories():
    response = requests.get(WP_URL + '/categories')
    if response.status_code == 200:
        print(response.text)
        with open('categories.json', 'w') as f:
            json.dump(response.json(), f)


# get_categories()

