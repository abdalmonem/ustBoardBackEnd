data = {
    "username": "ste7en",
    "password": "pass",
    "gendre": 0,
    "name": "Steven James"
}
print(data)
json_data = {
    "username": "ste7en95",
    "password": "new_pass",
    "gendre": 0,
    "name": "Steven J. O'Danold"
}


for key in data:
    if key in json_data:
        data[key] = json_data[key]
print("="*100)
print(data)

