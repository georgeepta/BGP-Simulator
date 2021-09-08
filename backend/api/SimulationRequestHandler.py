import json
import random
import psycopg2
import requests
from datetime import datetime, timezone
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from flask_restful import Api, Resource, reqparse
from backend.core.BGPtopology import BGPtopology



class SimulationRequestHandler(Resource):

    def launch_simulation(self, Topo, sim_data, simulation_uuid, conn):

        print('Simulation started')
        simulation_step = 0
        RESULTS = []
        counter = 0

        while counter < sim_data['nb_of_sims']:
            print('simulation step: ' + str(100 * simulation_step / sim_data['nb_of_sims']) + '%\r', end='')
            simulation_step += 1

            # do the legitimate announcement from the victim
            Topo.add_prefix(sim_data['legitimate_AS'], sim_data['legitimate_prefix'])
            simulation_RESULTS = {'before_hijack': {}, 'after_hijack': {}, 'after_mitigation': {}}  # "simulation_DATA" will contain the data to be saved as the output of the simulation
            simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix'] = Topo.get_nb_of_nodes_with_path_to_prefix(sim_data['legitimate_prefix'])
            simulation_RESULTS['before_hijack']['nb_of_nodes_with_hijacked_path_to_legitimate_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['legitimate_prefix'], sim_data['hijacker_AS'])

            if sim_data['hijack_prefix_type'] == "exact":

                # do the hijack from the hijacker
                if Topo.do_hijack(sim_data['hijacker_AS'], sim_data['hijacker_prefix'], sim_data['hijack_type']):
                    simulation_RESULTS['after_hijack']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    simulation_RESULTS['after_hijack']['list_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_list_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    simulation_RESULTS['after_hijack']['dict_of_nodes_and_infected_paths_to_hijacker_prefix'] = Topo.Get_path_to_prefix(sim_data['hijacker_prefix'], simulation_RESULTS['after_hijack']['list_of_nodes_with_hijacked_path_to_hijacker_prefix'])
                    simulation_RESULTS['after_hijack']['impact_estimation'] = simulation_RESULTS['after_hijack']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] / simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix']

                    # do the mitigation by anycasting the prefix from helper ASes (assuming they will attract traffic and then tunnel it to the victim)
                    for anycast_AS in sim_data['anycast_ASes']:
                        Topo.add_prefix(anycast_AS, sim_data['hijacker_prefix'])
                    simulation_RESULTS['after_mitigation']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])

                else:
                    # the hijack attempt failed --> repeat the simulation
                    Topo.clear_routing_information()
                    simulation_step = simulation_step - 1
                    continue

            else:

                # do the hijack from the hijacker
                simulation_RESULTS['before_hijack']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])

                if Topo.do_subprefix_hijack(sim_data['hijacker_AS'], sim_data['legitimate_prefix'], sim_data['hijacker_prefix'], sim_data['hijack_type']):
                    simulation_RESULTS['after_hijack']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])

                    # do the mitigation by anycasting the mitigation prefix from victim AS + helper ASes
                    # (assuming they will attract traffic and then tunnel it to the victim)

                    Topo.add_prefix(sim_data['legitimate_AS'], sim_data['mitigation_prefix'])
                    for anycast_AS in sim_data['anycast_ASes']:
                        Topo.add_prefix(anycast_AS, sim_data['mitigation_prefix'])
                    simulation_RESULTS['after_mitigation']['nb_of_nodes_with_hijacked_path_to_mitigation_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['mitigation_prefix'], sim_data['hijacker_AS'])

                else:
                    # the hijack attempt failed --> repeat the simulation
                    Topo.clear_routing_information()
                    simulation_step = simulation_step - 1
                    continue

            simulation_RESULTS['hijacker_AS'] = sim_data['hijacker_AS']
            simulation_RESULTS['legitimate_AS'] = sim_data['legitimate_AS']


            RESULTS.append(simulation_RESULTS)
            Topo.clear_routing_information()

            counter = counter + 1


        '''
        Insert simulation results in database
        '''
        self.insert_simulation_results_in_db(RESULTS, simulation_uuid, conn)

        '''
        Write the results to a json file
        '''
        print('Writing statistics to json...')
        jsonfilename = '../tests/results/statistics__CAIDA' + sim_data['caida_as_graph_dataset'] + '_sims' + str(sim_data['nb_of_sims']) + '_hijackType' + str(
            sim_data['hijack_type']) + '_test_hijacker' + '_.json'
        with open(jsonfilename, 'w') as jsonfile:
            json.dump(RESULTS, jsonfile)


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


    def set_rpki_rov(self, Topo, sim_data):
        if sim_data['rpki_rov_mode'] == "all":
            print("RPKI ROV mode --> all")
            for asn in Topo.get_all_nodes_ASNs():
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


    def connect_to_db(self, db_name, user, password, host, port):
        # establishing the connection
        conn = psycopg2.connect(
            database=db_name, user=user, password=password, host=host, port=port
        )

        '''
        psycopg2 is Python DB API-compliant, so the auto-commit feature is off by default. 
        We need to set conn.autocommit to True to commit any pending transaction to the database.
        '''
        conn.autocommit = True

        return conn


    def insert_simulation_data_in_db(self, sim_data, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing SQL queries to INSERT a record into the database.
        sql = '''
              INSERT INTO BGP_HIJACKING_SIMULATIONS(simulation_status, simulation_data, sim_start_time, num_of_simulations, num_of_finished_simulations)
              VALUES (%s, %s, %s, %s, %s) RETURNING simulation_id''';

        cursor.execute(sql, ('Pending', json.dumps(sim_data), datetime.now(timezone.utc), sim_data['nb_of_sims'], 0))

        simulation_uuid = cursor.fetchone()[0]
        print("Simulation UUID: " + simulation_uuid)
        print("Simulation data inserted in db........")
        return simulation_uuid


    def insert_simulation_results_in_db(self, sim_results, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''
              UPDATE BGP_HIJACKING_SIMULATIONS SET simulation_results = simulation_results || %s ::jsonb
              WHERE simulation_id=%s
           ''';

        for result in sim_results:
            cursor.execute(sql, (json.dumps(result), simulation_uuid))
        print("Simulation results inserted in db........")


    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('simulation_type', type=str, help="Simulation type is required (custom or as-vulnerability or country-vulnerability)")
        req_parser.add_argument('legitimate_AS', type=int, help="ASN of victim is required (e.g., 12345)")
        req_parser.add_argument('legitimate_prefix', type=str, help="CIDR prefix of victim is required (e.g., 1.2.3.0/24)")
        req_parser.add_argument('hijacker_AS', type=int, help="ASN of hijacker is required (e.g., 67890)")
        req_parser.add_argument('hijacker_prefix', type=str, help="CIDR prefix of hijacker is required (e.g., 1.2.3.0/24)")
        req_parser.add_argument('hijack_type', type=int, help="Must be an integer in {0,1,2,3,...} denoting the type of hijacking attack, with 0 = origin AS attack , 1 = 1st hop attack, etc.")
        req_parser.add_argument('hijack_prefix_type', type=str, help="Must be a string in {exact, subprefix} denoting exact or subprefix announcement")
        req_parser.add_argument('anycast_ASes', type=list, location='json', help="Must be a list of integers denoting the ASNs of the helper ASes (e.g., [12345, 67890, ...])")
        req_parser.add_argument('mitigation_prefix', type=str, help="CIDR mitigation prefix that is going to announced by helper AS and victim AS (e.g., 1.2.3.0/25)")
        req_parser.add_argument('realistic_rpki_rov', type=bool, help="A boolean variable denoting if the simulation should use the most recent from the RIR databases with the help of the Routinator or just to make theoretical assumptions for the RPKI ROV")
        req_parser.add_argument('rpki_rov_mode', type=str, help="Must be a string denoting the RPKI Route Origin Validation mode (e.g., disabled, all, 20%, ...")
        req_parser.add_argument('nb_of_sims', type=int, help="An integer denoting the number of experiment runs (repetitions) of the simulation")
        req_parser.add_argument('caida_as_graph_dataset', type=str, help="A string of type yyyymmdd denoting the CAIDA AS-graph dataset from which the topology will be loaded")
        req_parser.add_argument('caida_ixps_datasets', type=str, help="A string of type yyyymm denoting the CAIDA IXPs datasets (ix-asns_yyyymm.jsonl and ixs_yyyymm.jsonl) from which the topology generate the links between AS-IXPS")
        req_parser.add_argument('max_nb_anycast_ASes', type=int, help="An integer denoting the maximum number of anycast ASes to be used for hijack mitigation")

        sim_data = req_parser.parse_args()

        '''
        create a connection to the database
        '''
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')

        '''
        insert simulation data in database
        '''
        simulation_uuid = self.insert_simulation_data_in_db(sim_data, conn)

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
        self.set_rpki_rov_table(Topo, sim_data, "http://localhost:9556/api/v1/validity/")

        '''
        Launch simulation
        '''
        self.launch_simulation(Topo, sim_data, simulation_uuid, conn)

        '''
        close connection to database
        '''
        conn.close()

        return {
            'simulation_type': sim_data
        }