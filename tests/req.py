import requests


url = "https://api.quotable.io/random"

res = requests.get(url)

print(res.json())
