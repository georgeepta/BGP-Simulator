import psycopg2


def create_db():
   # establishing the connection
   conn = psycopg2.connect(
      database="postgres", user='gepta', password='1821', host='127.0.0.1', port='5432'
   )

   '''
   psycopg2 is Python DB API-compliant, so the auto-commit feature is off by default. 
   We need to set conn.autocommit to True to commit any pending transaction to the database.
   '''
   conn.autocommit = True

   # Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   # Preparing query to create a database
   sql = '''CREATE database BGP_Simulator''';

   # Creating a database
   cursor.execute(sql)
   print("Database BGP_Simulator created successfully........")

   # Closing the connection
   conn.close()


def create_bgp_hijacking_sims_table():
   # Establishing the connection
   conn = psycopg2.connect(
      database="bgp_simulator", user='gepta', password='1821', host='127.0.0.1', port='5432'
   )

   '''
   psycopg2 is Python DB API-compliant, so the auto-commit feature is off by default. 
   We need to set conn.autocommit to True to commit any pending transaction to the database.
   '''
   conn.autocommit = True

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
      num_of_finished_simulations INTEGER,
      sim_start_time TIMESTAMPTZ,
      sim_end_time TIMESTAMPTZ, 
      PRIMARY KEY (simulation_id)
   )''';
   cursor.execute(sql)
   print("Table BGP_HIJACKING_SIMULATIONS created successfully........")

   # Closing the connection
   conn.close()


def insert_data():
   # Establishing the connection
   conn = psycopg2.connect(
      database="bgp_simulator", user='gepta', password='1821', host='127.0.0.1', port='5432'
   )
   # Setting auto commit false
   conn.autocommit = True

   # Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   # Preparing SQL queries to INSERT a record into the database.
   sql = '''
      INSERT INTO BGP_HIJACKING_SIMULATIONS(simulation_status, simulation_data, sim_start_time, sim_end_time, num_of_simulations, num_of_finished_simulations)
      VALUES (%s, %s, %s, %s, %s, %s) RETURNING simulation_id''';

   cursor.execute(sql, ('Pending', '{"victim_AS": "11888", "victim_prefix": "1.2.3.4/22", "hijacker_AS": "13335", "hijacker_prefix": "1.2.3.4/24"}',
      '2021-08-22 21:17:25-07', '2021-08-22 21:27:25-07', 100, 55 ))

   simulation_uuid = cursor.fetchone()[0]
   print("simulation uuid: " + simulation_uuid)

   sql2 = '''
      UPDATE BGP_HIJACKING_SIMULATIONS SET simulation_results = simulation_results || %s ::jsonb
      WHERE simulation_id=%s
   ''';

   cursor.execute(sql2, ('{"num_of_infected_ASes": "45000", "list_of_infected_ASes": [13243, 43325, 53423], "impact": "64%"}', simulation_uuid))

   # Commit your changes in the database
   conn.commit()
   print("Records inserted........")

   # Closing the connection
   conn.close()


def select_data():
   # Establishing the connection
   conn = psycopg2.connect(
      database="bgp_simulator", user='gepta', password='1821', host='127.0.0.1', port='5432'
   )
   # Setting auto commit false
   conn.autocommit = True

   # Creating a cursor object using the cursor() method
   cursor = conn.cursor()

   # Retrieving data
   cursor.execute('''SELECT simulation_id, 
                            simulation_status,
                            simulation_data, 
                            num_of_simulations,
                            num_of_finished_simulations,
                            sim_start_time,
                            sim_end_time
                     FROM BGP_HIJACKING_SIMULATIONS''')

   # Fetching 1st row from the table
   #result = cursor.fetchone();
   #print(result)

   # Fetching all rows from the table
   result = cursor.fetchall()
   print(result)

   # Commit your changes in the database
   conn.commit()

   # Closing the connection
   conn.close()


if __name__ == '__main__':
   #create_db()
   #create_bgp_hijacking_sims_table()
   #insert_data()
   select_data()
