import psycopg2
from flask_restful import Resource, reqparse

class SimulationDetailsRequestHandler(Resource):

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


    def select_simulation_from_db(self, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''SELECT json_agg(json_build_object(
           'simulation_id',simulation_id,
           'simulation_status', simulation_status,
           'simulation_data', simulation_data,
           'simulation_results', simulation_results,
           'num_of_simulations', num_of_simulations,
           'num_of_repetitions', num_of_repetitions,
           'num_of_finished_simulations', num_of_finished_simulations,
           'sim_start_time', sim_start_time,
           'sim_end_time', sim_end_time)) 
        FROM BGP_HIJACKING_SIMULATIONS 
        WHERE simulation_id=%s
        '''

        # Retrieving data
        cursor.execute(sql, (simulation_uuid,))

        # Fetching all rows from the table
        sim_details = cursor.fetchall()[0][0][0]

        asns_details_dict = {}

        for result in sim_details["simulation_results"]:
            asn_list = [] #result["anycast_ASes"] TODO: Important !!! should be added
            asn_list.extend([result["legitimate_AS"], result["hijacker_AS"]])
            for asn in asn_list:
                if asn not in asns_details_dict:
                    sql2 = '''SELECT asn_to_org_data FROM ASN_TO_ORG WHERE asn=%s''';
                    # Retrieving data
                    cursor.execute(sql2, (asn,))
                    asn_details = cursor.fetchall()[0][0]
                    asns_details_dict[asn] = asn_details

        sim_details["asns_details"] = asns_details_dict

        return sim_details


    def get(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('simulation_uuid', type=str, required=True, help="Give the unique UUID of the simulation.")
        simulation_uuid = req_parser.parse_args()['simulation_uuid']

        '''
        create a connection to the database
        '''
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')

        '''
        Fetch everything for the requested simulation from db
        '''
        result = self.select_simulation_from_db(simulation_uuid, conn)

        '''
        close connection to database
        '''
        conn.close()

        return result, 200

