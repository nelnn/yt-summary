import requests

from rich import print

resp = requests.get("https://noembed.com/embed?url=https://www.youtube.com/watch?v=ipRvjS7q1DI&t=199").json()
print(resp)
