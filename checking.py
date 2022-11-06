import json
import requests
from wp_api.operation import WP_URL, auth

filename = 'plaguetale.jpg'
data = open(filename, 'rb').read()
headers = {"Content-Disposition": f'attachment; filename="{filename}"',
           "Accept": "application/json"}

res = requests.post(WP_URL + '/media', auth=auth, headers=headers, data=data)
with open('x.json', 'w') as f:
    json.dump(res.json(), f)

print(res.json())