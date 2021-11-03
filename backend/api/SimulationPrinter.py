import json
import psycopg2
from datetime import datetime, timezone

class SimulationPrinter:

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


    def print_results_in_json_file(self, simulation_uuid, sim_data, conn):
        '''
        Write the results to a json file for debugging purposes
        '''

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Retrieving data
        cursor.execute('''SELECT simulation_results FROM BGP_HIJACKING_SIMULATIONS WHERE simulation_id=%s''', (simulation_uuid,))

        # Fetching all rows from the table
        results = cursor.fetchall()[0][0]

        print('Writing statistics to json...')
        jsonfilename = '../tests/results/statistics__' + str(simulation_uuid) + '__CAIDA' + sim_data['caida_as_graph_dataset'] + '_sims' + str(
            sim_data['nb_of_sims']) + '_hijackType' + str(sim_data['hijack_type']) + '_test_hijacker' + '_.json'
        #jsonfilename = '../evaluation/evaluation_data/Historical-Hijacks/subprefix-hijacks/'+str(sim_data['hist_hijack_id'])+'_sim_'+str(sim_data['legitimate_AS'])+"_"+str(sim_data['hijacker_AS'])+'.json'
        with open(jsonfilename, 'w') as jsonfile:
            json.dump(results, jsonfile)



    def update_simulation_status(self, status, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''
            UPDATE BGP_HIJACKING_SIMULATIONS SET simulation_status=%s
            WHERE simulation_id=%s 
        ''';

        cursor.execute(sql, (status, simulation_uuid))


    def update_simulation_end_time(self, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''
            UPDATE BGP_HIJACKING_SIMULATIONS SET sim_end_time=%s
            WHERE simulation_id=%s 
        ''';

        cursor.execute(sql, (datetime.now(timezone.utc), simulation_uuid))



    def isLastRepetition(self, simulation_uuid, sim_data, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        sql = '''
                   SELECT num_of_finished_simulations FROM BGP_HIJACKING_SIMULATIONS 
                   WHERE simulation_id=%s 
               ''';

        cursor.execute(sql, (simulation_uuid,))
        num_of_finished_simulations = cursor.fetchone()[0]

        if num_of_finished_simulations == (sim_data['nb_of_sims'] * sim_data['nb_of_reps']):
            print("Last Repetition ...")
            return True
        else:
            return False

    def save_statistics(self, simulation_uuid, sim_data):
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')
        if self.isLastRepetition(simulation_uuid, sim_data, conn):
            self.update_simulation_status('Completed', simulation_uuid, conn)
            self.update_simulation_end_time(simulation_uuid, conn)
            self.print_results_in_json_file(simulation_uuid, sim_data, conn)
        conn.close()