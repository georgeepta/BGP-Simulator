from flask_restful import Api, Resource, reqparse

class SimulationRequestHandler(Resource):
    def post(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('simulation_type', type=str, help="Simulation type is required (Manual or AS_Valnerability)")

        '''
        simulation_type = input_data['simulation_type']
        legitimate_AS = input_data['legitimate_AS']
        legitimate_prefix = input_data['legitimate_prefix']
        hijacker_AS = input_data['hijacker_AS']
        hijacker_prefix = input_data['hijacker_prefix']
        hijack_type = input_data['hijack_type']
        hijack_prefix_type = input_data['hijack_prefix_type']
        anycast_ASes = input_data['anycast_ASes']
        rpki_rov_mode = input_data['rpki_rov_mode']
        nb_of_sims = input_data['nb_of_sims']
        dataset = input_data['dataset']
        max_nb_anycast_ASes = input_data['max_nb_anycast_ASes']
        '''

        return {
            'message': 'Post handled'
        }