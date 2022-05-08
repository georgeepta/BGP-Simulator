import json
import time
import random
import requests

def read_json_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0

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


def launch_random_prefix_hijacks(num_of_sims):
    print("### Random Simulation Starts.... ###")
    sim_data = {
        "simulation_type": "random",
        "legitimate_AS": 0,
        "legitimate_prefix": "1.2.3.0/24",
        "hijacker_AS": 0,
        "hijacker_prefix": "1.2.3.0/24",
        "hijack_type": 0,
        "hijack_prefix_type": "exact",
        "anycast_ASes": [0],
        "mitigation_prefix": "1.2.3.0/24",
        "rpki_rov_mode": "rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare",
        "nb_of_sims": 50,
        "nb_of_reps": 1,
        "caida_as_graph_dataset": "20220401",
        "caida_ixps_datasets": "202110",
        "max_nb_anycast_ASes": 2,
        "realistic_rpki_rov": False
    }
    if num_of_sims >= 50:
        for sim in range(1, (num_of_sims//50) + 1):
            response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
            print(response.json())
            time.sleep(16 * 60)  # after 16 mins do the next request
        if (num_of_sims % 50) != 0:
            sim_data["nb_of_sims"] = num_of_sims % 50
            response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
            print(response.json())
    else:
        sim_data["nb_of_sims"] = num_of_sims
        response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
        print(response.json())



def launch_prefix_hijack_to_greek_ASes_from_2hop_plus_ASes(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes, isGreekASesHijackers):

    if isGreekASesHijackers:
        print("### Custom Simulation Starts (prefix hijacks to greek ASes from 2hop+ ASes).... ###")
    else:
        print("### Custom Simulation Starts (prefix hijacks to greek ASes from 2hop+ ASes - no greek ASes as hijackers).... ###")

    all_greek_ASNs = set()
    all_greek_ASNs_prefixes_dict = {}
    for json_obj in greek_ASes_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]
    for json_obj in ASes_present_in_greece_plus_greek_ixps_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]

    all_ASNs_in_Graph_list = AS_relationships_Graph.keys()
    for ASN in all_greek_ASNs:
        if ASN in all_ASNs_in_Graph_list:
            providers_list = AS_relationships_Graph[ASN]["providers"]
            peers_list = AS_relationships_Graph[ASN]["peers"]
            customers_list = AS_relationships_Graph[ASN]["customers"]
            no_hijacker_ASes_list = list(map(str, providers_list + peers_list + customers_list))
            if isGreekASesHijackers:
                #All greek ASes that are 1 hop plus away are candidate hijackers
                #excluding the victim AS from the candidate hijackers
                no_hijacker_ASes_list.append(ASN)
            else:
                #All greek ASes that are 1 hop plus away are not candidate hijackers
                #including the victim AS
                no_hijacker_ASes_list = list(set(no_hijacker_ASes_list).union(all_greek_ASNs))

            candidate_hijacker_ASes_list = [int(asn) for asn in all_ASNs_in_Graph_list if asn not in no_hijacker_ASes_list]
            pfx = random.sample(all_greek_ASNs_prefixes_dict[ASN], 1)

            for hijacker_AS in random.sample(candidate_hijacker_ASes_list, 2):
                sim_data = {
                    "simulation_type": "custom",
                    "legitimate_AS": int(ASN),
                    "legitimate_prefix": pfx,
                    "hijacker_AS": hijacker_AS,
                    "hijacker_prefix": pfx,
                    "hijack_type": 0,
                    "hijack_prefix_type": "exact",
                    "anycast_ASes": [5511],  # Orange S.A we dont care about that field in these experiments
                    "mitigation_prefix": pfx,
                    "rpki_rov_mode": "rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare",
                    "nb_of_sims": 10, #in custom sims change this for more repetitions
                    "nb_of_reps": 1,
                    "caida_as_graph_dataset": "20220401",
                    "caida_ixps_datasets": "202110",
                    "max_nb_anycast_ASes": 1,
                    "realistic_rpki_rov": True
                }
                print(sim_data)
                response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
                print(response.json())
                time.sleep(5 * 60)  # after 5 mins do the next request



def launch_prefix_hijack_to_greek_ASes_from_1hop_ASes_no_customers(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes, isGreekASesHijackers):

    if isGreekASesHijackers:
        print("### Custom Simulation Starts (prefix hijacks to greek ASes from 1hop ASes no customers).... ###")
    else:
        print("### Custom Simulation Starts (prefix hijacks to greek ASes from 1hop ASes no customers - no greek ASes as hijackers).... ###")

    all_greek_ASNs = set()
    all_greek_ASNs_prefixes_dict = {}
    for json_obj in greek_ASes_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]
    for json_obj in ASes_present_in_greece_plus_greek_ixps_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]

    all_ASNs_in_Graph_list = AS_relationships_Graph.keys()
    for ASN in all_greek_ASNs:
        if ASN in all_ASNs_in_Graph_list:
            providers_list = list(map(str, AS_relationships_Graph[ASN]["providers"]))
            peers_list = list(map(str, AS_relationships_Graph[ASN]["peers"]))
            #customers_list = list(map(str, AS_relationships_Graph[ASN]["customers"]))

            candidate_hijacker_ASes_list = providers_list + peers_list
            if not isGreekASesHijackers:
                # All greek ASes that are 1 hop away are not candidate hijackers
                # including the victim AS
                candidate_hijacker_ASes_list = [int(asn) for asn in candidate_hijacker_ASes_list if asn not in all_greek_ASNs]

            pfx = random.sample(all_greek_ASNs_prefixes_dict[ASN], 1)
            if len(candidate_hijacker_ASes_list) <= 2:
                final_hijacker_ASes_list = candidate_hijacker_ASes_list
            else:
                final_hijacker_ASes_list = random.sample(candidate_hijacker_ASes_list, 2)

            for hijacker_AS in final_hijacker_ASes_list:
                sim_data = {
                    "simulation_type": "custom",
                    "legitimate_AS": int(ASN),
                    "legitimate_prefix": pfx,
                    "hijacker_AS": hijacker_AS,
                    "hijacker_prefix": pfx,
                    "hijack_type": 0,
                    "hijack_prefix_type": "exact",
                    "anycast_ASes": [5511],  # Orange S.A we dont care about that field in these experiments
                    "mitigation_prefix": pfx,
                    "rpki_rov_mode": "rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare",
                    "nb_of_sims": 10, #in custom sims change this for more repetitions
                    "nb_of_reps": 1,
                    "caida_as_graph_dataset": "20220401",
                    "caida_ixps_datasets": "202110",
                    "max_nb_anycast_ASes": 1,
                    "realistic_rpki_rov": True
                }
                print(sim_data)
                response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
                print(response.json())
                time.sleep(5 * 60)  # after 5 mins do the next request



def launch_prefix_hijack_from_greek_ASes_to_greek_ASes(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes):

    print("### Custom Simulation Starts (prefix hijack from greek ASes to greek ASes).... ###")

    all_greek_ASNs = set()
    all_greek_ASNs_prefixes_dict = {}
    for json_obj in greek_ASes_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]
    for json_obj in ASes_present_in_greece_plus_greek_ixps_and_prefixes:
        all_greek_ASNs.add(str(json_obj["asn"]))
        all_greek_ASNs_prefixes_dict[str(json_obj["asn"])] = json_obj["prefixes"]

    all_ASNs_in_Graph_list = AS_relationships_Graph.keys()
    for ASN in all_greek_ASNs:
        if ASN in all_ASNs_in_Graph_list:
            candidate_hijacker_ASes_list = list(map(int, all_greek_ASNs))
            candidate_hijacker_ASes_list.remove(int(ASN))

            pfx = random.sample(all_greek_ASNs_prefixes_dict[ASN], 1)
            for hijacker_AS in random.sample(candidate_hijacker_ASes_list, 2):
                sim_data = {
                    "simulation_type": "custom",
                    "legitimate_AS": int(ASN),
                    "legitimate_prefix": pfx,
                    "hijacker_AS": hijacker_AS,
                    "hijacker_prefix": pfx,
                    "hijack_type": 0,
                    "hijack_prefix_type": "exact",
                    "anycast_ASes": [5511],  # Orange S.A we dont care about that field in these experiments
                    "mitigation_prefix": pfx,
                    "rpki_rov_mode": "rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare",
                    "nb_of_sims": 10, #in custom sims change this for more repetitions
                    "nb_of_reps": 1,
                    "caida_as_graph_dataset": "20220401",
                    "caida_ixps_datasets": "202110",
                    "max_nb_anycast_ASes": 1,
                    "realistic_rpki_rov": True
                }
                print(sim_data)
                response = requests.post('http://127.0.0.1:5000/launch_simulation', json=sim_data)
                print(response.json())
                time.sleep(5 * 60)  # after 5 mins do the next request




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

    ### Useful functions for the project signed with the Greek ministry (Greek Internet Observatory)
    AS_relationships_Graph = read_json_data(r'../evaluation/evaluation_data/forth_ypourgeio_project/AS_Relations_Graph_CAIDA.json')
    greek_ASes_and_prefixes = read_json_data(r'../evaluation/evaluation_data/forth_ypourgeio_project/all_greek_prefixes_2.json')
    ASes_present_in_greece_plus_greek_ixps_and_prefixes = read_json_data(r'../evaluation/evaluation_data/forth_ypourgeio_project/all_ngreek_asns_greek_ixps.json')

    launch_random_prefix_hijacks(2000)
    launch_prefix_hijack_to_greek_ASes_from_2hop_plus_ASes(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes, True)
    launch_prefix_hijack_to_greek_ASes_from_1hop_ASes_no_customers(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes, False)
    launch_prefix_hijack_from_greek_ASes_to_greek_ASes(AS_relationships_Graph, greek_ASes_and_prefixes, ASes_present_in_greece_plus_greek_ixps_and_prefixes)