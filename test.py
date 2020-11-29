import requests

BASE = "http://127.0.0.1:5000/"

data = [ {"name": "Flask tutorial", "likes": 10, "views": 10000},
         {"name": "Heroku Tutoria", "likes": 120, "views": 90600},
         {"name": "Django tutorial", "likes": 450, "views": 12000}
        ]

for i in range(len(data)):
    response = requests.post(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.patch(BASE + "video/1", {"name":"Heroku Tutorial", "likes": 899})
print(response.json())
response = requests.get(BASE + "video/1")
print(response.json())
response = requests.delete(BASE + "video/2")
print(response.json())

