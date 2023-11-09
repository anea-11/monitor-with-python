import requests

response = requests.get('my-url')
if response.status_code == 200:
    print("App is healthy")
else:
    print("App is not healthy")

