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

'''
get all simulation events from db [GET]
curl -X GET -H "Content-Type: application/json" http://localhost:5000/simulation_events
'''

'''
get all info for a specific simulation [GET]
curl -X GET "http://localhost:5000/simulation_details?simulation_uuid=a5d3c351-bfd8-40be-ae25-e0c1912c5b7e"
'''
