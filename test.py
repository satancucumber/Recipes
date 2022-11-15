import requests
url = "http://127.0.0.1:5000/favorite"
request = 2

r = requests.get(url, user_id = 2)

print(r.content.decode())
print(r)