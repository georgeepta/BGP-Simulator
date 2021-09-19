import requests


'''
launch simulation [POST]
curl -X POST -H "Content-Type: application/json" -d "@input_data.json" http://localhost:5000/launch_simulation
'''
response = requests.post('http://127.0.0.1:5000/launch_simulation', json={'key': 'value'})
print(response.headers)
print(response.json())

'''
as_vulnerability_ranking [GET]
curl -X GET -H "Content-Type: application/json" -d "@as_vuln_rank_data.json" http://localhost:5000/as_vulnerability_ranking
'''
