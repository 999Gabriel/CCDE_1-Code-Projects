import requests
r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
print(r)

print(r.status_code)
print((r.headers['Content-Type']))
print(r.json())
print(r.text)

j = r.json()
for i in j:
    print(i['title'])