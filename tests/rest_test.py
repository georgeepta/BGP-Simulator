import requests


'''
launch simulation [POST]
'''
response = requests.post('http://127.0.0.1:5000/launch_simulation', json={'key': 'value'})
print(response.headers)
print(response.json())