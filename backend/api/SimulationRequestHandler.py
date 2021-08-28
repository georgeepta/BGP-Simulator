import random
from flask_restful import Api, Resource, reqparse
from backend.core.BGPtopology import BGPtopology


class SimulationRequestHandler(Resource):

    def set_rpki_rov(self, Topo, sim_data):
        if sim_data['rpki_rov_mode'] == "all":
            print("RPKI ROV mode --> all")
            for asn in Topo.get_all_nodes_ASNs():
                Topo.get_node(asn).rov = True
        elif sim_data['rpki_rov_mode'] == "20%":
            pass
        return

    def set_rpki_rov_table(self, Topo, sim_data):
        # In type 1,2,3,...,N hijacks, the origin AS, in the AS_PATH that the hijacker announce to its neighbors,
        # is always the victim AS !!! For this reason, the rov_table contains only entries for the hijacker, victim and helper ASes
        # Outdated --> (Furthermore, we assume that the victim and helper ASes mitigate the subprefix attack by announcing the same subprefix
        # as the hijacker (e.g., the hijacker announces the longest subprefix that is permissible)).

        rpki_rov_table = {}

        if sim_data['realistic_rpki_rov'] == False:
            print("Hypothetical ROV")
            rpki_rov_table[(sim_data['legitimate_AS'], sim_data['legitimate_prefix'])] = random.choice(["valid", "not-found"])
            rpki_rov_table[(sim_data['legitimate_AS'], sim_data['mitigation_prefix'])] = random.choice(["valid", "not-found"])
            rpki_rov_table[(sim_data['hijacker_AS'], sim_data['hijacker_prefix'])] = random.choice(["invalid", "not-found"])
            for helper in sim_data['anycast_ASes']:
                rpki_rov_table[(helper, sim_data['mitigation_prefix'])] = random.choice(["valid", "not-found"])

            for asn in Topo.get_all_nodes_ASNs():
                Topo.get_node(asn).rpki_validation = rpki_rov_table

            for entry in rpki_rov_table:
                print(entry, rpki_rov_table[entry])

        else:
            pass

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
        self.set_rpki_rov_table(Topo, sim_data)



        return {
            'simulation_type': sim_data
        }