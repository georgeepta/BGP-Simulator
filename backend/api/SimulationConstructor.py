import os
import csv
import json
import random
import requests
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from backend.core.BGPtopology import BGPtopology
from backend.api.SimulationWorker import SimulationWorker
from backend.api.SimulationPrinter import SimulationPrinter
from mpipe import UnorderedWorker


class SimulationConstructor(UnorderedWorker):

    '''
    Performs RPKI Route Origin Validation, by quering the Routinator's (open source RPKI Relying Party software)
    HTTP API endpoint running on a server (e.g., localhost on port 9556)

    It concatenates the endpoint_url, origin_asn, prefix arguments in a single url string and sends an GET request to the API.
    IF the returned HTTP status code is 200:
        return the validity state of this route announcement (valid, invalid, or not found)
    ELSE:
        return the HTTP status code (we dont have any data that indicate the validity of the route announcement)

    Input arguments:
        (a) endpoint_url: the endpoint's URL which is used for Route Origin Validation
            e.g., in our case http://localhost:9556/api/v1/validity/
        (b) origin_asn: the origin AS number of the route announcement (in AS_PATH)
        (c) prefix: the prefix of the route announcement

    Returns:
        The validity state of this route announcement (valid, invalid, or not found)
        IF the returned HTTP status code is 200, ELSE the HTTP status code
    '''

    def do_rov(self, endpoint_url, origin_asn, prefix):
        url = endpoint_url + str(origin_asn) + "/" + prefix
        routinator_adapter = HTTPAdapter(max_retries=3)
        session = requests.Session()
        # Use `routinator_adapter` for all requests to endpoints that start with the endpoint_url argument
        session.mount(endpoint_url, routinator_adapter)
        try:
            response = session.get(url, timeout=3)
        except ConnectionError as ce:
            print(ce)
        except Timeout:
            print('The request timed out')
        else:
            # print('The request did not time out')
            if response.status_code == 200:
                # Successful GET request
                # print(response.json())
                return response.json()["validated_route"]["validity"]["state"]
            else:
                # HTTP Response not contains useful data for the ROV
                return response.status_code


    def load_ROV_Deployment_monitor_data(self, file_path):
        asn_do_rov_list = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Columns names are {", ".join(row)}')
                    line_count += 1
                else:
                    print("ASN: " + row[0], "AS Name: " + row[1], "Certainty: " + row[2])
                    if float(row[2]) >= 0.5:
                        asn_do_rov_list.append(int(row[0]))
                    line_count += 1
            print(f'Processed: {line_count} lines.')
            print(asn_do_rov_list)
        return asn_do_rov_list


    def load_ROV_Active_Measurements_data(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            # use the Total Unique ROV (Fully+Partially filtering) result
            asn_do_rov_list = [int(item) for item in data["2"][129]]
            print(asn_do_rov_list)
            return asn_do_rov_list


    def load_TMA_paper_2021_Rodday_union_ROV_Deployment_monitor_union_IsBGPSafeYetCloudflare_data(self, file_path):
        with open(file_path) as json_file:
            asn_do_rov_list = json.load(json_file)["union_ROV_ASes_of_all_datasets_list"]
            print(asn_do_rov_list)
            return asn_do_rov_list



    def load_ASRank_data(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data


    def generate_rpki_rov_list(self, num_of_top_isp_rpki_adopters, rpki_adoption_propability, top_500_ASRank_ASNs):
        n_top_ISPs = int(num_of_top_isp_rpki_adopters / rpki_adoption_propability)
        set_of_n_top_ISPs = top_500_ASRank_ASNs["data"]["asns"]["edges"][0:n_top_ISPs]
        list_of_n_top_ASNs = []
        for item in set_of_n_top_ISPs:
            list_of_n_top_ASNs.append(int(item["node"]["asn"]))
        return random.sample(list_of_n_top_ASNs, num_of_top_isp_rpki_adopters)


    def set_rpki_rov(self, Topo, sim_data):
        if sim_data['rpki_rov_mode'] == "all":
            print("RPKI ROV mode --> all")
            for asn in Topo.get_all_nodes_ASNs():
                Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "rov_deployment_monitor":
            print("RPKI ROV mode --> rov_deployment_monitor")
            rov_deployment_monitor_list = self.load_ROV_Deployment_monitor_data("../datasets/ROV-Deployment-Monitor/2020-08-31.csv")
            for asn in rov_deployment_monitor_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "rov_active_measurements":
            print("RPKI ROV mode --> rov_active_measurements")
            rov_active_measurements_list = self.load_ROV_Active_Measurements_data("../datasets/ROV-Active-Measurements-TMA-Paper/20210719_resultset_asns.json")
            for asn in rov_active_measurements_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "manual":
            print("RPKI ROV mode --> manual")
            top_500_ASRank_ASNs = self.load_ASRank_data("../datasets/ASRank/top_500_ASNs.json")
            top_random_ISPs_list = self.generate_rpki_rov_list(sim_data['num_of_top_isp_rpki_adopters'], sim_data['rpki_adoption_propability'], top_500_ASRank_ASNs)
            print(top_random_ISPs_list)
            for asn in top_random_ISPs_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "today_rov_status+other_random_prop":
            print("RPKI ROV mode --> today_rov_status+other_random_prop")
            rov_active_measurements_list = self.load_ROV_Active_Measurements_data("../datasets/ROV-Active-Measurements-TMA-Paper/20210719_resultset_asns.json")
            tmp_rov_list = [item for item in Topo.get_all_nodes_ASNs() if item not in rov_active_measurements_list]
            if sim_data['other_random_prop'] == 0:
                other_rov_list = []
            else:
                other_rov_list = random.sample(tmp_rov_list, int(len(tmp_rov_list) * sim_data['other_random_prop']))
            final_rov_list = rov_active_measurements_list + other_rov_list
            for asn in final_rov_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "top_isps_rov+other_random_prop":
            print("RPKI ROV mode --> top_isps_rov+other_random_prop")
            top_500_ASRank_ASNs = self.load_ASRank_data("../datasets/ASRank/top_500_ASNs.json")
            top_rov_ISPs_list = self.generate_rpki_rov_list(sim_data['num_of_top_isp_rpki_adopters'],
                                                               sim_data['rpki_adoption_propability'],
                                                               top_500_ASRank_ASNs)
            tmp_rov_list = [item for item in Topo.get_all_nodes_ASNs() if item not in top_rov_ISPs_list]
            if sim_data['other_random_prop'] == 0:
                other_rov_list = []
            else:
                other_rov_list = random.sample(tmp_rov_list, int(len(tmp_rov_list) * sim_data['other_random_prop']))
            final_rov_list = top_rov_ISPs_list + other_rov_list
            for asn in final_rov_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "random_20":
            print("RPKI ROV mode --> Random 20%")
            all_BGP_nodes_list = Topo.get_all_nodes_ASNs()
            random_20_BGP_nodes_list = random.sample(all_BGP_nodes_list, int(len(all_BGP_nodes_list) * 0.2))
            for asn in random_20_BGP_nodes_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare":
            print("RPKI ROV mode --> rov_active_measurements+rov_deployment_monitor+isBgpSafeYet_cloudflare")
            ROV_ASes_union_list = self.load_TMA_paper_2021_Rodday_union_ROV_Deployment_monitor_union_IsBGPSafeYetCloudflare_data("../evaluation/evaluation_data/forth_ypourgeio_project/ROV_ASes_InTodaysInternet_results.json")
            for asn in ROV_ASes_union_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True

        return


    def set_rpki_rov_table(self, Topo, sim_data, validator_url):
        # In type 1,2,3,...,N hijacks, the origin AS, in the AS_PATH that the hijacker announce to its neighbors,
        # is always the victim AS !!! For this reason, the rov_table contains only entries for the hijacker, victim and helper ASes
        # Outdated --> (Furthermore, we assume that the victim and helper ASes mitigate the subprefix attack by announcing the same subprefix
        # as the hijacker (e.g., the hijacker announces the longest subprefix that is permissible)).

        rpki_rov_table = {}

        if sim_data['realistic_rpki_rov'] == False:
            print("Hypothetical ROV")
            rpki_rov_table[(sim_data['legitimate_AS'], sim_data['legitimate_prefix'])] = random.choice(["valid", "not-found"])
            rpki_rov_table[(sim_data['legitimate_AS'], sim_data['hijacker_prefix'])] = random.choice(["valid", "not-found"]) #useful for type 1, 2, 3 ..., N attacks
            rpki_rov_table[(sim_data['legitimate_AS'], sim_data['mitigation_prefix'])] = random.choice(["valid", "not-found"])
            rpki_rov_table[(sim_data['hijacker_AS'], sim_data['hijacker_prefix'])] = random.choice(["invalid", "not-found"])
            for helper in sim_data['anycast_ASes']:
                rpki_rov_table[(helper, sim_data['mitigation_prefix'])] = random.choice(["valid", "not-found"])

        else:
            print("Realistic ROV")
            AS_to_validate = []
            AS_to_validate.append((sim_data['legitimate_AS'], sim_data['legitimate_prefix']))
            AS_to_validate.append((sim_data['legitimate_AS'], sim_data['hijacker_prefix'])) #useful for type 1, 2, 3 ..., N attacks
            AS_to_validate.append((sim_data['legitimate_AS'], sim_data['mitigation_prefix']))
            AS_to_validate.append((sim_data['hijacker_AS'], sim_data['hijacker_prefix']))
            for helper in sim_data['anycast_ASes']:
                AS_to_validate.append((helper, sim_data['mitigation_prefix']))
            AS_to_validate = list(set([i for i in AS_to_validate])) #remove duplicates from the list
            for item in AS_to_validate:
                origin_AS = item[0]
                origin_prefix = item[1]
                validity_state = self.do_rov(validator_url, origin_AS, origin_prefix)
                rpki_rov_table[(origin_AS, origin_prefix)] = validity_state

        '''
        Set the rpki rov table, only if the BGPnode performs ROV 
        '''
        for asn in Topo.get_all_nodes_ASNs():
            if Topo.get_node(asn).rov == True:
                Topo.get_node(asn).rpki_validation = rpki_rov_table

        for entry in rpki_rov_table:
            print(entry, rpki_rov_table[entry])

        return rpki_rov_table


    def load_create_Topology(self, Topo, sim_data):
        '''
        load and create topology
        '''
        print('Loading topology...')
        Topo.load_topology_from_csv(
            '../datasets/CAIDA AS-graph/serial-2/' + os.environ.get("AS_GRAPH_SERIAL2_DATASET_DATE") + '.as-rel2.txt')
        Topo.load_ixps_from_json('../datasets/CAIDA IXPS/' + 'ixs_' + os.environ.get("IXPS_DATASET_DATE") + '.jsonl',
                                 '../datasets/CAIDA IXPS/' + 'ix-asns_' + os.environ.get("IXPS_DATASET_DATE") + '.jsonl')
        Topo.add_extra_p2p_custom_links()


    def doTask(self, task_data):

        sim_data = task_data["sim_data"]
        simulation_uuid = task_data["simulation_uuid"]

        '''
        load and create topology
        '''
        Topo = BGPtopology()
        self.load_create_Topology(Topo, sim_data)

        '''
        Set the ASes that are going to do RPKI Route Origin Validation, 
        according to user preference (rpki_rov_mode)
        '''
        self.set_rpki_rov(Topo, sim_data)

        '''
        Set the RPKI ROV table for each AS that do ROV, 
        according to user preference (realistic_rpki_rov -> realistic or hypothetical) 
        '''
        rpki_rov_table = self.set_rpki_rov_table(Topo, sim_data, os.environ.get("ROOTINATOR_ROV_URL"))

        '''
        Launch simulation
        '''
        sw = SimulationWorker()
        sw.start(Topo, sim_data, rpki_rov_table, simulation_uuid)

        '''
        Update some statistic fields in db for the simulation and save simulation results into json file
        (only if, it is the last repetition of all simulations)
        '''
        sp = SimulationPrinter()
        sp.save_statistics(simulation_uuid, sim_data)