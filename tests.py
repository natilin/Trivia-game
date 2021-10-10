import requests
import json
r = requests.get('https://s3.eu-west-1.amazonaws.com/data.cyber.org.il/virtual_courses/network.py/chapter_4/redirectionPage.html')
r.json()
print(r)