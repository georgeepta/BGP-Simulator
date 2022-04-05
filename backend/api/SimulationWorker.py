import os
import json
import psycopg2

class SimulationWorker:

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


    def update_num_of_finished_sims(self, simulation_uuid, conn):
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql = '''
               UPDATE BGP_HIJACKING_SIMULATIONS SET num_of_finished_simulations = num_of_finished_simulations + 1 
               WHERE simulation_id=%s 
           ''';

        cursor.execute(sql, (simulation_uuid,))


    def save_rov_table_in_sim_results(self, simulation_RESULTS, rpki_rov_table):

        simulation_RESULTS.update({'rpki_rov_table': {}})
        for entry in rpki_rov_table:
            if simulation_RESULTS['rpki_rov_table'].get(entry[0]) == None:
                simulation_RESULTS['rpki_rov_table'].update({entry[0]: {entry[1]: rpki_rov_table[entry]}})
            else:
                simulation_RESULTS['rpki_rov_table'][entry[0]].update({entry[1]: rpki_rov_table[entry]})


    def impact_estimation_after_mitigation(self, Topo, sim_data, simulation_RESULTS):
        if sim_data['hijacker_prefix'] == sim_data['mitigation_prefix']:
            return self.impact_estimation_after_hijack(Topo, sim_data, simulation_RESULTS)
        else:
            nb_of_nodes_with_path_to_mitigation_prefix = Topo.get_nb_of_nodes_with_path_to_prefix(
                IPprefix=sim_data['mitigation_prefix'],
                list_of_nodes=simulation_RESULTS['before_hijack']['list_of_nodes_with_path_to_legitimate_prefix']
            )
            nb_of_nodes_with_hijacked_path_to_mitigation_prefix = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(
                sim_data['mitigation_prefix'],
                sim_data['hijacker_AS'],
                simulation_RESULTS['before_hijack']['list_of_nodes_with_path_to_legitimate_prefix']
            )
            if simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix'] > 0:
                return 1 - ((nb_of_nodes_with_path_to_mitigation_prefix - nb_of_nodes_with_hijacked_path_to_mitigation_prefix) / simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix'])
            else:
                return 0


    def impact_estimation_after_hijack(self, Topo, sim_data, simulation_RESULTS):
        nb_of_nodes_with_hijacked_path_to_hijacker_prefix = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(
            sim_data['hijacker_prefix'],
            sim_data['hijacker_AS'],
            simulation_RESULTS['before_hijack']['list_of_nodes_with_path_to_legitimate_prefix']
        )
        if simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix'] > 0:
            return nb_of_nodes_with_hijacked_path_to_hijacker_prefix / simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix']
        else:
            return 0


    def launch_simulation(self, Topo, sim_data, rpki_rov_table, simulation_uuid, conn):

        simulation_step = 0
        RESULTS = []
        counter = 0

        while counter < sim_data['nb_of_reps']:

            simulation_step += 1

            # do the legitimate announcement from the victim
            Topo.add_prefix(sim_data['legitimate_AS'], sim_data['legitimate_prefix'])
            simulation_RESULTS = {'before_hijack': {}, 'after_hijack': {}, 'after_mitigation': {}}  # "simulation_DATA" will contain the data to be saved as the output of the simulation
            simulation_RESULTS['before_hijack']['nb_of_nodes_with_path_to_legitimate_prefix'] = Topo.get_nb_of_nodes_with_path_to_prefix(sim_data['legitimate_prefix'])
            simulation_RESULTS['before_hijack']['list_of_nodes_with_path_to_legitimate_prefix'] = Topo.get_list_of_nodes_with_path_to_prefix(sim_data['legitimate_prefix'])
            simulation_RESULTS['before_hijack']['nb_of_nodes_with_hijacked_path_to_legitimate_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['legitimate_prefix'], sim_data['hijacker_AS'])

            if sim_data['hijack_prefix_type'] == "exact":

                # do the hijack from the hijacker
                if Topo.do_hijack(sim_data['hijacker_AS'], sim_data['hijacker_prefix'], sim_data['hijack_type']):
                    simulation_RESULTS['after_hijack']['nb_of_nodes_with_hijacked_path_to_hijacker_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    simulation_RESULTS['after_hijack']['dict_of_nodes_and_infected_paths_to_hijacker_prefix'] = Topo.Get_path_to_prefix(
                        sim_data['hijacker_prefix'],
                        Topo.get_list_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    )
                    simulation_RESULTS['after_hijack']['impact_estimation'] = self.impact_estimation_after_hijack(Topo, sim_data, simulation_RESULTS)

                    # do the mitigation by anycasting the prefix from helper ASes (assuming they will attract traffic and then tunnel it to the victim)
                    for anycast_AS in sim_data['anycast_ASes']:
                        Topo.add_prefix(anycast_AS, sim_data['hijacker_prefix'])
                    simulation_RESULTS['after_mitigation']['nb_of_nodes_with_hijacked_path_to_mitigation_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    simulation_RESULTS['after_mitigation']['dict_of_nodes_and_infected_paths_to_mitigation_prefix'] = Topo.Get_path_to_prefix(
                        sim_data['hijacker_prefix'],
                        Topo.get_list_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    )
                    simulation_RESULTS['after_mitigation']['impact_estimation'] = self.impact_estimation_after_mitigation(Topo, sim_data, simulation_RESULTS)

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
                    simulation_RESULTS['after_hijack']['dict_of_nodes_and_infected_paths_to_hijacker_prefix'] = Topo.Get_path_to_prefix(
                        sim_data['hijacker_prefix'],
                        Topo.get_list_of_nodes_with_hijacked_path_to_prefix(sim_data['hijacker_prefix'], sim_data['hijacker_AS'])
                    )
                    simulation_RESULTS['after_hijack']['impact_estimation'] = self.impact_estimation_after_hijack(Topo, sim_data, simulation_RESULTS)

                    # do the mitigation by anycasting the mitigation prefix from victim AS + helper ASes
                    # (assuming they will attract traffic and then tunnel it to the victim)

                    Topo.add_prefix(sim_data['legitimate_AS'], sim_data['mitigation_prefix'])
                    for anycast_AS in sim_data['anycast_ASes']:
                        Topo.add_prefix(anycast_AS, sim_data['mitigation_prefix'])
                    simulation_RESULTS['after_mitigation']['nb_of_nodes_with_hijacked_path_to_mitigation_prefix'] = Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(sim_data['mitigation_prefix'], sim_data['hijacker_AS'])
                    simulation_RESULTS['after_mitigation']['dict_of_nodes_and_infected_paths_to_mitigation_prefix'] = Topo.Get_path_to_prefix(
                        sim_data['mitigation_prefix'],
                        Topo.get_list_of_nodes_with_hijacked_path_to_prefix(sim_data['mitigation_prefix'], sim_data['hijacker_AS'])
                    )
                    simulation_RESULTS['after_mitigation']['impact_estimation'] = self.impact_estimation_after_mitigation(Topo, sim_data, simulation_RESULTS)

                else:
                    # the hijack attempt failed --> repeat the simulation
                    Topo.clear_routing_information()
                    simulation_step = simulation_step - 1
                    continue

            simulation_RESULTS['hijacker_AS'] = sim_data['hijacker_AS']
            simulation_RESULTS['legitimate_AS'] = sim_data['legitimate_AS']
            simulation_RESULTS['anycast_ASes'] = sim_data['anycast_ASes']
            simulation_RESULTS['ASes_that_do_ROV'] = Topo.get_list_of_nodes_that_do_rov()
            self.save_rov_table_in_sim_results(simulation_RESULTS, rpki_rov_table)

            RESULTS.append(simulation_RESULTS)
            Topo.clear_routing_information()
            self.update_num_of_finished_sims(simulation_uuid, conn)

            counter = counter + 1

        '''
        Insert simulation results in database
        '''
        self.insert_simulation_results_in_db(RESULTS, simulation_uuid, conn)


    def start(self, Topo, sim_data, rpki_rov_table, simulation_uuid):
        conn = self.connect_to_db(os.environ.get("DB_NAME"),
                                  os.environ.get("DB_USERNAME"),
                                  os.environ.get("DB_PASS"),
                                  os.environ.get("DB_IP"),
                                  os.environ.get("DB_PORT"))
        self.launch_simulation(Topo, sim_data, rpki_rov_table, simulation_uuid, conn)
        conn.close()
