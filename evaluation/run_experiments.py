import time
import requests


def compute_collateral_benefit(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list):
    print("### Collateral benefit ###")
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


def compute_today_rov_status_other_random_prop(num_of_top_isp_rpki_adopters, rpki_adoption_propability, other_random_prop_list):
    print("### Today ROV status + Other ASes ###")
    for prop_value in other_random_prop_list:
        print("Today ROV status: " + str(num_of_top_isp_rpki_adopters) + " , Deployment Probability of other ASes: " + str(prop_value))
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
            "rpki_rov_mode": "today_rov_status+other_random_prop",
            "nb_of_sims": 20,
            "nb_of_reps": 1,
            "caida_as_graph_dataset": "20211001",
            "caida_ixps_datasets": "202107",
            "max_nb_anycast_ASes": 2,
            "realistic_rpki_rov": False,
            "num_of_top_isp_rpki_adopters": num_of_top_isp_rpki_adopters,
            "rpki_adoption_propability": rpki_adoption_propability,
            "other_random_prop": prop_value
        }
        response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
        print(response.json())
        time.sleep(10 * 60)  # after 10 mins do the next request



def compute_top_isps_rov_other_random_prop(num_of_top_isp_rpki_adopters, rpki_adoption_propability, other_random_prop_list):
    print("### Top ISPs ROV + Other ASes ###")
    for prop_value in other_random_prop_list:
        print("Top ISPs ROV number: " + str(
            num_of_top_isp_rpki_adopters) + " , Deployment Probability of other ASes: " + str(prop_value))
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
            "rpki_rov_mode": "top_isps_rov+other_random_prop",
            "nb_of_sims": 20,
            "nb_of_reps": 1,
            "caida_as_graph_dataset": "20211001",
            "caida_ixps_datasets": "202107",
            "max_nb_anycast_ASes": 2,
            "realistic_rpki_rov": False,
            "num_of_top_isp_rpki_adopters": num_of_top_isp_rpki_adopters,
            "rpki_adoption_propability": rpki_adoption_propability,
            "other_random_prop": prop_value
        }
        response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
        print(response.json())
        time.sleep(10 * 60)  # after 10 mins do the next request


def send_random_sim_request():
    sim_data = {
        "simulation_type": "random",
        "legitimate_AS": 0,
        "legitimate_prefix": "x.y.z.w/m",
        "hijacker_AS": 0,
        "hijacker_prefix": "x.y.z.w/m",
        "hijack_type": 0,
        "hijack_prefix_type": "exact",
        "anycast_ASes": [2],
        "mitigation_prefix": "x.y.z.w/m",
        "rpki_rov_mode": "rov_active_measurements+rov_deployment_monitor",
        "nb_of_sims": 50,
        "nb_of_reps": 1,
        "caida_as_graph_dataset": "20220401",
        "caida_ixps_datasets": "202110",
        "max_nb_anycast_ASes": 2,
        "realistic_rpki_rov": False
    }
    response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
    print(response.json())


def launch_random_sim(num_of_sims):
    print("### Random Simulation Starts.... ###")
    for sim in range(1, (num_of_sims//50) + 1):
        send_random_sim_request()
        time.sleep(17 * 60)  # after 17 mins do the next request
    if (num_of_sims % 50) != 0:
        send_random_sim_request()


if __name__ == '__main__':
    '''
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1]
    num_of_top_isp_rpki_adopters = list(range(0, 101, 10))
    other_random_prop_list = [v * 0.1 for v in range(0, 11, 1)]
    print("EXPERIMENTS START ...")
    #compute_collateral_benefit(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list)
    #compute_today_rov_status_other_random_prop(100, 1.0, other_random_prop_list)
    compute_top_isps_rov_other_random_prop(100, 1.0, other_random_prop_list)
    '''
    launch_random_sim(2000)