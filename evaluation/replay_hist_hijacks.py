import json
import time
import requests


def read_hijack_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0


def replay_prefix_hijacks():
    for num in list(range(1, 3, 1)):
        if num % 6 == 0:
            print("Sleep for 3 mins...")
            time.sleep(3 * 60)  # after 3 mins do the next request
        file_path = "./evaluation_data/Historical-Hijacks/prefix-hijacks/"+str(num)+".json"
        hijack_data = read_hijack_data(file_path)
        for victim in hijack_data["victims"]:
            for attacker in hijack_data["attackers"]:
                sim_data = {
                    "simulation_type": "custom",
                    "legitimate_AS": int(victim),
                    "legitimate_prefix": hijack_data["details"]["prefix"],
                    "hijacker_AS": int(attacker),
                    "hijacker_prefix": hijack_data["details"]["prefix"],
                    "hijack_type": 0,
                    "hijack_prefix_type": "exact",
                    "anycast_ASes": [5511], #Orange S.A we dont care about that field in these experiments
                    "mitigation_prefix": hijack_data["details"]["prefix"],
                    "rpki_rov_mode": "rov_active_measurements",
                    "nb_of_sims": 1,
                    "nb_of_reps": 1,
                    "caida_as_graph_dataset": "20211001",
                    "caida_ixps_datasets": "202107",
                    "max_nb_anycast_ASes": 1,
                    "realistic_rpki_rov": True,
                    "hist_hijack_id": num
                }
                print(sim_data)
                response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
                print(response.json())


def replay_subprefix_hijacks():
    for num in list(range(1, 2, 1)):
        if num % 6 == 0:
            print("Sleep for 3 mins...")
            time.sleep(3 * 60)  # after 3 mins do the next request
        file_path = "./evaluation_data/Historical-Hijacks/subprefix-hijacks/"+str(num)+".json"
        hijack_data = read_hijack_data(file_path)
        for victim in hijack_data["victims"]:
            for attacker in hijack_data["attackers"]:
                sim_data = {
                    "simulation_type": "custom",
                    "legitimate_AS": int(victim),
                    "legitimate_prefix": hijack_data["details"]["super_pfx"],
                    "hijacker_AS": int(attacker),
                    "hijacker_prefix": hijack_data["details"]["sub_pfx"],
                    "hijack_type": 0,
                    "hijack_prefix_type": "subprefix",
                    "anycast_ASes": [5511], #Orange S.A we dont care about that field in these experiments
                    "mitigation_prefix": hijack_data["details"]["sub_pfx"],
                    "rpki_rov_mode": "rov_active_measurements",
                    "nb_of_sims": 1,
                    "nb_of_reps": 1,
                    "caida_as_graph_dataset": "20211001",
                    "caida_ixps_datasets": "202107",
                    "max_nb_anycast_ASes": 1,
                    "realistic_rpki_rov": True,
                    "hist_hijack_id": num
                }
                print(sim_data)
                response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
                print(response.json())


if __name__ == '__main__':
    #replay_prefix_hijacks()
    replay_subprefix_hijacks()