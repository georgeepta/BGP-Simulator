import csv
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


    def set_rpki_rov(self, Topo, sim_data):
        if sim_data['rpki_rov_mode'] == "all":
            print("RPKI ROV mode --> all")
            for asn in Topo.get_all_nodes_ASNs():
                Topo.get_node(asn).rov = True
        if sim_data['rpki_rov_mode'] == "rov_deployment_monitor":
            print("RPKI ROV mode --> rov_deployment_monitor")
            rov_deployment_monitor_list = self.load_ROV_Deployment_monitor_data("../datasets/ROV-Deployment-Monitor/2020-08-31.csv")
            for asn in rov_deployment_monitor_list:
                if Topo.has_node(asn):
                    Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "20%":
            pass
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
            '../datasets/CAIDA AS-graph/serial-2/' + sim_data['caida_as_graph_dataset'] + '.as-rel2.txt')
        Topo.load_ixps_from_json('../datasets/CAIDA IXPS/' + 'ixs_' + sim_data['caida_ixps_datasets'] + '.jsonl',
                                 '../datasets/CAIDA IXPS/' + 'ix-asns_' + sim_data['caida_ixps_datasets'] + '.jsonl')
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
        rpki_rov_table = self.set_rpki_rov_table(Topo, sim_data, "http://localhost:9556/api/v1/validity/")

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