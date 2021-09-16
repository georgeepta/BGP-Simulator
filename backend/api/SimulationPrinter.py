import json
import psycopg2

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


    def update_progress_bar(self, sim_data, simulation_uuid):
        conn = self.connect_to_db("bgp_simulator", 'gepta', '1821', '127.0.0.1', '5432')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        sql = '''
               SELECT num_of_finished_simulations FROM BGP_HIJACKING_SIMULATIONS 
               WHERE simulation_id=%s 
           ''';

        cursor.execute(sql, (simulation_uuid,))
        num_of_finished_simulations = cursor.fetchone()[0]

        if sim_data['simulation_type'] == "custom":
            print('simulation step: ' + str(100 * num_of_finished_simulations / sim_data['nb_of_sims']) + '%\r', end='')
        else:
            print('simulation step: ' + str(100 * num_of_finished_simulations / (sim_data['nb_of_reps'] * sim_data['nb_of_sims'])) + '%\r', end='')
        return

    def print_results_in_json_file(self, sim_results, sim_data):
        '''
        Write the results to a json file
        '''
        print('Writing statistics to json...')
        jsonfilename = '../tests/results/statistics__CAIDA' + sim_data['caida_as_graph_dataset'] + '_sims' + str(
            sim_data['nb_of_sims']) + '_hijackType' + str(
            sim_data['hijack_type']) + '_test_hijacker' + '_.json'
        with open(jsonfilename, 'w') as jsonfile:
            json.dump(sim_results, jsonfile)

    def save_results(self, sim_results, sim_data):
        self.print_results_in_json_file(sim_results, sim_data)
        #self.update_progress_bar(task_results['sim_data'], task_results['simulation_uuid'])