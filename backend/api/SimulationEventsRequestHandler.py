import psycopg2
from flask_restful import Resource, reqparse

class SimulationEventsRequestHandler(Resource):

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


    def select_simulation_data_from_db(self,conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Retrieving data

        sql = '''SELECT json_agg(json_build_object(
           'simulation_id',simulation_id,
           'simulation_status', simulation_status,
           'simulation_data', simulation_data,
           'num_of_simulations', num_of_simulations,
           'num_of_repetitions', num_of_repetitions,
           'num_of_finished_simulations', num_of_finished_simulations,
           'sim_start_time', sim_start_time,
           'sim_end_time', sim_end_time))
              FROM BGP_HIJACKING_SIMULATIONS''';

        cursor.execute(sql)

        # Fetching all rows from the table
        results = cursor.fetchall()[0][0]

        return results


    def delete_simulation_from_db(self, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''
        DELETE FROM BGP_HIJACKING_SIMULATIONS
        WHERE simulation_id=%s
        RETURNING simulation_id
        ''';

        cursor.execute(sql, (simulation_uuid,))

        simulation_uuid = cursor.fetchone()[0]
        print('Simulation with UUID: ' + simulation_uuid + ' deleted permanently from db')
        return simulation_uuid


    def get(self):
        '''
        create a connection to the database
        '''
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')

        '''
        Fetch useful data for the simulation events table
        '''
        results = self.select_simulation_data_from_db(conn)

        '''
        close connection to database
        '''
        conn.close()

        return results, 200


    def delete(self):
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('simulation_uuid', type=str, required=True, help="Give the unique UUID of the simulation.")
        simulation_uuid = req_parser.parse_args()['simulation_uuid']

        '''
        create a connection to the database
        '''
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')

        '''
        Delete the requested simulation from db
        '''
        self.delete_simulation_from_db(simulation_uuid, conn)

        '''
        close connection to database
        '''
        conn.close()

        return {'message': 'Simulation with UUID: ' + simulation_uuid + ' deleted permanently from db'}, 200



