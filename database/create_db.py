import json
import psycopg2

class Init_Database():

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

   def read_json_data(self, file_path):
      try:
         with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
      except FileNotFoundError:
         print("Sorry, the file, " + file_path + " ,does not exist.")
         return 0

   def create_db(self, conn, db_name):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Preparing query to create a database
      sql = "CREATE database "+db_name+";"

      # Creating a database
      cursor.execute(sql)
      print("BPHS database created successfully........")


   def create_bgp_hijacking_sims_table(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Doping bgp_hijacking_simulations table if already exists.
      sql_drop = '''DROP TABLE IF EXISTS BGP_HIJACKING_SIMULATIONS''';
      cursor.execute(sql_drop)

      sql_extension = '''CREATE EXTENSION IF NOT EXISTS "uuid-ossp"''';
      cursor.execute(sql_extension)

      # Creating table as per requirement
      sql = '''CREATE TABLE BGP_HIJACKING_SIMULATIONS(
         simulation_id uuid DEFAULT uuid_generate_v4 (),
         simulation_status VARCHAR(20) NOT NULL,
         simulation_data json NOT NULL, 
         simulation_results jsonb NOT NULL DEFAULT '[]'::jsonb,
         num_of_simulations INTEGER NOT NULL,
         num_of_repetitions INTEGER NOT NULL,
         num_of_finished_simulations INTEGER,
         sim_start_time TIMESTAMPTZ,
         sim_end_time TIMESTAMPTZ, 
         PRIMARY KEY (simulation_id)
      )''';
      cursor.execute(sql)
      print("Table BGP_HIJACKING_SIMULATIONS created successfully........")


   def insert_data(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Preparing SQL queries to INSERT a record into the database.
      sql = '''
         INSERT INTO BGP_HIJACKING_SIMULATIONS(simulation_status, simulation_data, sim_start_time, sim_end_time, num_of_simulations, num_of_repetitions, num_of_finished_simulations)
         VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING simulation_id''';

      cursor.execute(sql, ('Pending', '{"victim_AS": "11888", "victim_prefix": "1.2.3.4/22", "hijacker_AS": "13335", "hijacker_prefix": "1.2.3.4/24"}',
         '2021-08-22 21:17:25-07', '2021-08-22 21:27:25-07', 100, 5, 55 ))

      simulation_uuid = cursor.fetchone()[0]
      print("simulation uuid: " + simulation_uuid)

      sql2 = '''
         UPDATE BGP_HIJACKING_SIMULATIONS SET simulation_results = simulation_results || %s ::jsonb
         WHERE simulation_id=%s
      ''';

      cursor.execute(sql2, ('{"num_of_infected_ASes": "45000", "list_of_infected_ASes": [13243, 43325, 53423], "impact": "64%"}', simulation_uuid))
      print("Records inserted........")


   def select_data(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Retrieving data
      cursor.execute('''SELECT simulation_results 
      FROM BGP_HIJACKING_SIMULATIONS 
      WHERE simulation_id=%s''', ("2a7e9b3a-d6f0-429d-8cce-1af8f2b6155e",))

      # Fetching 1st row from the table
      #result = cursor.fetchone();
      #print(result)

      # Fetching all rows from the table
      result = cursor.fetchall()
      self.print_results_in_json_file(result)


   def print_results_in_json_file(self, result):
      '''
      Write the results to a json file
      '''
      print('Writing statistics to json...')
      jsonfilename = '../tests/results/output.json'
      with open(jsonfilename, 'w') as jsonfile:
         json.dump(result, jsonfile)


   def select_data_as_json(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Retrieving data

      sql = '''SELECT json_agg(json_build_object(
      'simulation_id',simulation_id,
      'simulation_status', simulation_status,
      'simulation_data', simulation_data))
         FROM BGP_HIJACKING_SIMULATIONS''';

      cursor.execute(sql)

      # Fetching all rows from the table
      result = cursor.fetchall()[0][0]
      print(result)


   def create_asn_to_org_table(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Doping asn_to_org table if already exists.
      sql_drop = '''DROP TABLE IF EXISTS ASN_TO_ORG''';
      cursor.execute(sql_drop)

      # Creating table as per requirement
      sql = '''CREATE TABLE ASN_TO_ORG(
              asn INTEGER NOT NULL,
              asn_to_org_data json NOT NULL, 
              PRIMARY KEY (asn)
           )''';
      cursor.execute(sql)
      print("Table ASN_TO_ORG created successfully........")


   def create_As_To_Org_Dict(self, file_path):

      AS_dict = {}
      Org_dict = {}

      with open(file_path) as f:
         for line in f:
            data = json.loads(line)
            if data["type"] == "ASN":
               ASN = data.pop("asn", None)
               if ASN not in AS_dict:
                  AS_dict[ASN] = data
            elif data["type"] == "Organization":
               Org = data.pop("organizationId", None)
               if Org not in Org_dict:
                  Org_dict[Org] = data
            else:
               # invalid line
               pass

      # ASN to Organization mapping
      for ASN in AS_dict:
         org_id = AS_dict[ASN]["organizationId"]
         if org_id in Org_dict.keys():
            org_data = Org_dict[org_id]
            AS_dict[ASN]["organizationDetails"] = org_data

      return AS_dict


   def insert_data_asn_to_org(self, asn_to_org_dict, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Preparing SQL queries to INSERT a record into the database.
      sql = '''
               INSERT INTO ASN_TO_ORG(asn, asn_to_org_data)
               VALUES (%s, %s)''';

      for asn in asn_to_org_dict:
         cursor.execute(sql, (asn, json.dumps(asn_to_org_dict[asn])))

      print("Records inserted........")


   def selelect_asn_details(self, conn):
      # Creating a cursor object using the cursor() method
      cursor = conn.cursor()

      # Preparing SQL queries to INSERT a record into the database.
      sql = '''SELECT * FROM ASN_TO_ORG''';
      cursor.execute(sql)
      result = cursor.fetchall()
      print(result)
      asns_details_dict = {}
      for row in result:
         asns_details_dict[row[0]] = row[1]

      print(asns_details_dict)



if __name__ == '__main__':
   init_db = Init_Database()
   db_config_data = init_db.read_json_data('./config.json')
   conn = init_db.connect_to_db(db_config_data["default_postgres_db_name"],
                                db_config_data["db_user_username"],
                                db_config_data["db_user_password"],
                                db_config_data["dp_ip"],
                                db_config_data["dp_port"])
   init_db.create_db(conn, db_config_data["bphs_db_name"])
   conn.close()
   conn2 = init_db.connect_to_db(db_config_data["bphs_db_name"],
                                db_config_data["db_user_username"],
                                db_config_data["db_user_password"],
                                db_config_data["dp_ip"],
                                db_config_data["dp_port"])
   init_db.create_bgp_hijacking_sims_table(conn2)
   init_db.create_asn_to_org_table(conn2)
   print("Data insertion in ASN_TO_ORG table (duration ~10 minutes) Wait.........")
   init_db.insert_data_asn_to_org(init_db.create_As_To_Org_Dict('../datasets/AS-2-Orgs-mappings/'+db_config_data["asn_to_org_dataset_date"]+'.as-org2info.jsonl'), conn2)
   ### Test functions ###
   #init_db.insert_data(conn2)
   #init_db.select_data(conn2)
   #init_db.select_data_as_json(conn2)
   #init_db.selelect_asn_details(conn2)
   conn2.close()
