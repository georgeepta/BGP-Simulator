import json
import random
import psycopg2
import ipaddress
from copy import deepcopy
from datetime import datetime, timezone
from flask import Response
from flask_restful import Resource, reqparse
from backend.api.SimulationConstructor import SimulationConstructor
from mpipe import Pipeline, Stage
from backend.core.BGPtopology import BGPtopology



class SimulationRequestHandler(Resource):

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
              INSERT INTO BGP_HIJACKING_SIMULATIONS(simulation_status, simulation_data, sim_start_time, num_of_simulations, num_of_repetitions, num_of_finished_simulations)
              VALUES (%s, %s, %s, %s, %s, %s) RETURNING simulation_id''';

        cursor.execute(sql, ('In-Progress', json.dumps(sim_data), datetime.now(timezone.utc), sim_data['nb_of_sims'], sim_data['nb_of_reps'], 0))

        simulation_uuid = cursor.fetchone()[0]
        print("Simulation UUID: " + simulation_uuid)
        print("Simulation data inserted in db........")
        return simulation_uuid


    def load_create_Topology(self, Topo, sim_data):
        '''
        load and create topology
        '''
        print('Loading topology...')
        Topo.load_topology_from_csv(
            '../datasets/CAIDA AS-graph/serial-2/' + sim_data['caida_as_graph_dataset'] + '.as-rel2.txt')
        '''
        We comment the following lines, because are useful only if the members of the IXPs 
        that are not exists in the Topology are going to be insert in it.
        s 
        Topo.load_ixps_from_json('../datasets/CAIDA IXPS/' + 'ixs_' + sim_data['caida_ixps_datasets'] + '.jsonl',
                                 '../datasets/CAIDA IXPS/' + 'ix-asns_' + sim_data['caida_ixps_datasets'] + '.jsonl')
        Topo.add_extra_p2p_custom_links()
        '''

    def validate_ASN(self, ASN_List, ASN):
        if ASN in ASN_List:
            return ""
        else:
            return "ASN {} is not valid or unavailable for simulation.".format(ASN)

    def validate_IP_Address(self, prefix):
        try:
            ipaddress.ip_network(prefix)
            return ""
        except ValueError:
            return "IP prefix {} is not valid.".format(prefix)

    def validate_request_data(self, ASN_List, sim_data):
        isValidData = True
        errors_dict = {}
        if sim_data['simulation_type'] not in ["custom", "random"]:
            errors_dict['simulation_type'] = "Invalid simulation type --> type\"custom\" or \"random\""
        else:
            errors_dict['simulation_type'] = ""
            errors_dict['hijack_prefix_type'] = "" if sim_data['hijack_prefix_type'] in ["exact", "subprefix"] else "Invalid hijack attack --> type \"exact\" or \"subprefix\""
            errors_dict['rpki_rov_mode'] = "" if sim_data['rpki_rov_mode'] in ["all", "random_20", "rov_deployment_monitor", "rov_active_measurements", "manual", "today_rov_status+other_random_prop", "top_isps_rov+other_random_prop"] else "Invalid RPKI ROV MODE --> type \"all\" or \"random_20\""
            #It is not required to validate the following inputs:
            #hijack_type, caida_as_graph_dataset, caida_ixps_datasets, realistic_rpki_rov
            #nb_of_sims, nb_of_reps, max_nb_anycast_ASes

            if sim_data['simulation_type'] == "custom":
                errors_dict['legitimate_AS'] = self.validate_ASN(ASN_List, sim_data['legitimate_AS'])
                errors_dict['hijacker_AS'] = self.validate_ASN(ASN_List, sim_data['hijacker_AS'])
                anycast_err_str = ""
                for asn in sim_data['anycast_ASes']:
                    if asn not in ASN_List:
                        anycast_err_str += str(asn) + ","
                errors_dict['anycast_ASes'] = "" if anycast_err_str == "" else "ASN " + anycast_err_str + " not valid or unavailable for simulation."
                errors_dict['legitimate_prefix'] = self.validate_IP_Address(sim_data['legitimate_prefix'])
                errors_dict['hijacker_prefix'] = self.validate_IP_Address(sim_data['hijacker_prefix'])
                errors_dict['mitigation_prefix'] = self.validate_IP_Address(sim_data['mitigation_prefix'])

        for item in errors_dict:
            if errors_dict[item] != "":
                print("Invalid simulation data in the POST request!")
                isValidData = False
                break

        return isValidData, errors_dict


    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('simulation_type', type=str, required=True, help="Simulation type is required (custom or as-vulnerability or country-vulnerability)")
        req_parser.add_argument('legitimate_AS', type=int, help="ASN of victim is required (e.g., 12345)")
        req_parser.add_argument('legitimate_prefix', type=str, help="CIDR prefix of victim is required (e.g., 1.2.3.0/24)")
        req_parser.add_argument('hijacker_AS', type=int, help="ASN of hijacker is required (e.g., 67890)")
        req_parser.add_argument('hijacker_prefix', type=str, help="CIDR prefix of hijacker is required (e.g., 1.2.3.0/24)")
        req_parser.add_argument('hijack_type', type=int, required=True, help="Must be an integer in {0,1,2,3,...} denoting the type of hijacking attack, with 0 = origin AS attack , 1 = 1st hop attack, etc.")
        req_parser.add_argument('hijack_prefix_type', type=str, required=True, help="Must be a string in {exact, subprefix} denoting exact or subprefix announcement")
        req_parser.add_argument('anycast_ASes', type=list, location='json', help="Must be a list of integers denoting the ASNs of the helper ASes (e.g., [12345, 67890, ...])")
        req_parser.add_argument('mitigation_prefix', type=str, help="CIDR mitigation prefix that is going to announced by helper AS and victim AS (e.g., 1.2.3.0/25)")
        req_parser.add_argument('realistic_rpki_rov', type=bool, required=True, help="A boolean variable denoting if the simulation should use the most recent from the RIR databases with the help of the Routinator or just to make theoretical assumptions for the RPKI ROV")
        req_parser.add_argument('rpki_rov_mode', type=str, required=True, help="Must be a string denoting the RPKI Route Origin Validation mode (e.g., disabled, all, 20%, ...")
        req_parser.add_argument('nb_of_sims', type=int, required=True, help="An integer denoting the number of simulations")
        req_parser.add_argument('nb_of_reps', type=int, required=True, help="An integer denoting the number of experiment runs (repetitions) of each simulation")
        req_parser.add_argument('caida_as_graph_dataset', type=str, help="A string of type yyyymmdd denoting the CAIDA AS-graph dataset from which the topology will be loaded")
        req_parser.add_argument('caida_ixps_datasets', type=str, help="A string of type yyyymm denoting the CAIDA IXPs datasets (ix-asns_yyyymm.jsonl and ixs_yyyymm.jsonl) from which the topology generate the links between AS-IXPS")
        req_parser.add_argument('max_nb_anycast_ASes', type=int, required=True, help="An integer denoting the maximum number of anycast ASes to be used for hijack mitigation")
        req_parser.add_argument('num_of_top_isp_rpki_adopters', type=int, help="An Integer denoting the top N ISPs (according to ASRank) that do RPKI Route Origin Validation")
        req_parser.add_argument('rpki_adoption_propability', type=float, help="A float number denoting the propability that someone of the top N ISPs (according to ASRank) do RPKI Route Origin Validation")
        req_parser.add_argument('other_random_prop', type=float, help="A float number denoting the propability that a BGPNode do RPKI Route Origin Validation and this node a) not belongs in the top N ISPs (according to ASRank) or b) not belongs in the ASes that do ROV according to the todays Deployment")
        req_parser.add_argument('hist_hijack_id', type=int, help="An integer denoting the number of the file that contains the data of the historical hijack")


        sim_data = req_parser.parse_args()

        '''
        Initiaze a Topology and get the list of all ASNs: 
        useful for the validation and random simulations  
        '''
        Topo = BGPtopology()
        self.load_create_Topology(Topo, sim_data)
        ASN_List = Topo.get_all_nodes_ASNs()
        del Topo

        '''
        Validate POST request data
        '''
        isValidData, errors_dict = self.validate_request_data(ASN_List, sim_data)

        if isValidData:

            '''
            create a connection to the database
            '''
            conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')

            '''
            insert simulation data in database
            '''
            simulation_uuid = self.insert_simulation_data_in_db(sim_data, conn)

            '''
            close connection to database
            '''
            conn.close()

            '''
            Instantiate the BGP Hijacking Simulations
            '''

            Stage1 = Stage(worker_class=SimulationConstructor, size=2, do_stop_task=True, disable_result=False)
            pipe = Pipeline(Stage1)

            print('Simulation started')
            if sim_data['simulation_type'] == "custom":
                for task in range(0, sim_data['nb_of_sims']):
                    task_data = {"simulation_uuid": simulation_uuid, "sim_data": sim_data}
                    pipe.put(task_data)
                ## Term signal
                pipe.put(None)

            else:
                for task in range(0, sim_data['nb_of_sims']):
                    '''
                    Full randomness at each simulation
                    '''
                    random_ASNs = random.sample(ASN_List, 2 + sim_data['max_nb_anycast_ASes'])
                    sim_data['legitimate_AS'] = random_ASNs[0]
                    sim_data['hijacker_AS'] = random_ASNs[1]
                    sim_data['anycast_ASes'] = random_ASNs[2:]
                    '''
                    Alternative selection (victim, hijacker of this simulation are not available on the other simulations)
                    
                    sim_data['legitimate_AS'] = ASN_List.pop(random.randrange(len(ASN_List)))
                    sim_data['hijacker_AS'] = ASN_List.pop(random.randrange(len(ASN_List)))
                    sim_data['anycast_ASes'] = random.sample(ASN_List, sim_data['max_nb_anycast_ASes'])                
                    '''
                    task_data = {"simulation_uuid": simulation_uuid, "sim_data": deepcopy(sim_data)}
                    pipe.put(task_data)

                ## Term signal
                pipe.put(None)


            return {'status': "Simulation start!"}, 200

        else:
            response = Response(response=json.dumps(errors_dict), status=400, mimetype='application/json')
            return response