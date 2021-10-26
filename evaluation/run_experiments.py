import time
import requests

if __name__ == '__main__':
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1]
    num_of_top_isp_rpki_adopters = list(range(0, 101, 10))
    print("EXPERIMENTS START ...")
    for rpki_adopters_value in num_of_top_isp_rpki_adopters:
        for rpki_adoption_propability in rpki_adoption_propability_list:
            print("Top ISP RPKI Adopters: " + str(rpki_adopters_value) + " , RPKI Adoption Propability: " + str(rpki_adoption_propability))
            sim_data = {
                "simulation_type": "random",
                "legitimate_AS": 0,
                "legitimate_prefix": "x.y.z.w/m",
                "hijacker_AS": 0,
                "hijacker_prefix": "x.y.z.w/m",
                "hijack_type": 0,
                "hijack_prefix_type": "exact",
                "anycast_ASes": [0],
                "mitigation_prefix": "x.y.z.w/m",
                "rpki_rov_mode": "manual",
                "nb_of_sims": 20,
                "nb_of_reps": 1,
                "caida_as_graph_dataset": "20211001",
                "caida_ixps_datasets": "202107",
                "max_nb_anycast_ASes": 2,
                "realistic_rpki_rov": False,
                "num_of_top_isp_rpki_adopters": rpki_adopters_value,
                "rpki_adoption_propability": rpki_adoption_propability
            }
            response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
            print(response.json())
            time.sleep(8 * 60) #after 8mins do the next request