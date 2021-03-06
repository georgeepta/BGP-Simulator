#!/usr/bin/env python3
#
#
# Author: Georgios Eptaminitakis
# University of Crete, Greece
#
# E-mail: gepta@csd.uoc.gr
#
#


#import time
import random
import sys
import csv
import json
sys.path.insert(0, '/home/george/UOC-CSD/MASTER/master_thesis/BGP-Simulator/')
from backend.core.BGPtopology import BGPtopology





'''
A script that (i) does a number of hijacking simulations with anycast mitigation, (ii) saves the results (in pkl type), and (iii) write some main information from the results to a csv file.

Input (command-line) arguments:
	(a) nb_of_sims: an integer denoting the number of experiment runs (repetitions) of the simulation
	(b) hijack_prefix_type: a string denoting exact or subprefix announcement 
	(c) hijack_type: an integer in {0,1,2,3,...} denoting the type of hijacking attack, with 0 = origin AS attack , 1 = 1st hop attack, etc.
	(d) dataset: an integer of type yyyymmdd denoting the dataset from which the topology will be loaded
	(e) max_nb_anycast_ASes: an integer denoting the maximum number of anycast ASes to be used for hijack mitigation

Topologies are stored in the "../CAIDA AS-graph/serial-2/" folder.

The csv is formatted as follows:
'''



'''
read the input arguments; if incorrect arguments, exit
'''

if len(sys.argv) is 2:
	input_data_file_name = sys.argv[1]
else:
	sys.exit("Incorrent arguments. Arguments should be {input_data_file_name}")


with open(input_data_file_name, 'r') as jsonfile:
	input_data = json.load(jsonfile)
	simulation_type = input_data['simulation_type']
	legitimate_AS  = input_data['legitimate_AS']
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
load and create topology
'''
print('Loading topology...')
Topo = BGPtopology()
Topo.load_topology_from_csv('../datasets/CAIDA AS-graph/serial-2/'+dataset+'.as-rel2.txt')
Topo.load_ixps_from_json('../datasets/CAIDA IXPS/'+"ixs_202104.jsonl", '../datasets/CAIDA IXPS/'+"ix-asns_202104.jsonl")
Topo.add_extra_p2p_custom_links()

'''
Select which ASes are going to do RPKI Route Origin Validation
and set a rov table for testing purposes
'''
for asn in Topo.get_all_nodes_ASNs():
	Topo.get_node(asn).rov = True
	Topo.get_node(asn).rpki_validation = {("24409", "1.2.4.0/24") : "not-found",
								("24409", "1.2.4.0/25"): "not-found",
                       			("38803", "1.2.4.0/24") : "not-found",
								("38803", "1.2.4.0/25"): "not-found",
                       			("24151", "1.2.4.0/24"): "not-found",
								("24151", "1.2.4.0/25"): "not-found",
                       			("24406", "1.2.4.0/24"): "not-found",
								("24406", "1.2.4.0/25"): "not-found",
								}



'''
add to the topology the list of RIPE monitors (i.e., ASNs of the members of the RIPE RIS route collectors)
'''


'''
do simulations:
	for each run, 
	(i) select randomly a legitimate and a hijacking AS, and X anycast ASes (where X = max_nb_anycast_ASes)
	(ii) add a new prefix to the legitimate AS (BGP messages for the prefix will start propagating)
	(iii) hijack the prefix from the hijacker AS
'''
print('Simulation started')
list_of_ASNs = Topo.get_all_nodes_ASNs()
simulation_step = 0
DATA = []
counter = 0

while counter < nb_of_sims:
	print('simulation step: '+str(100*simulation_step/nb_of_sims)+'%\r',end='')
	simulation_step += 1

	# randomly select victim, hijacker, anycasters (for mitigation)
	'''
	r = random.sample(list_of_ASNs,2+max_nb_anycast_ASes)
	legitimate_AS = r[0]
	hijacker_AS = r[1]
	anycast_ASes = r[2:]
	prefix = "1.0.0.0/24"
	subprefix = "10.1.0.0/24"
	'''

	# do the legitimate announcement from the victim
	Topo.add_prefix(legitimate_AS,legitimate_prefix)
	simulation_DATA = []	# "simulation_DATA" will contain the data to be saved as the output of the simulation
	simulation_DATA.append(Topo.get_nb_of_nodes_with_path_to_prefix(legitimate_prefix))
	simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(legitimate_prefix,hijacker_AS))

	if hijack_prefix_type == "exact":

		# do the hijack from the hijacker
		if Topo.do_hijack(hijacker_AS,hijacker_prefix,hijack_type):
			simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(hijacker_prefix, hijacker_AS))

			# do the mitigation by anycasting the prefix from helper ASes (assuming they will attract traffic and then tunnel it to the victim)
			for anycast_AS in anycast_ASes:
				Topo.add_prefix(anycast_AS, hijacker_prefix)
			simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(hijacker_prefix, hijacker_AS))
		else:
			# the hijack attempt failed --> repeat the simulation
			Topo.clear_routing_information()
			simulation_step = simulation_step - 1
			continue

	else:

		# do the hijack from the hijacker
		simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(hijacker_prefix, hijacker_AS))

		if Topo.do_subprefix_hijack(hijacker_AS, legitimate_prefix, hijacker_prefix, hijack_type):
			simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(hijacker_prefix, hijacker_AS))

			# do the mitigation by anycasting the prefix from helper ASes (assuming they will attract traffic and then tunnel it to the victim)

			#the simplest case: helper ASes + victim announce the same prefix as the hijacker (max length)
			Topo.add_prefix(legitimate_AS, hijacker_prefix)
			for anycast_AS in anycast_ASes:
				Topo.add_prefix(anycast_AS, hijacker_prefix)
			simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(hijacker_prefix, hijacker_AS))
		else:
			# the hijack attempt failed --> repeat the simulation
			Topo.clear_routing_information()
			simulation_step = simulation_step - 1
			continue


	simulation_DATA.append(hijacker_AS)
	simulation_DATA.append(legitimate_AS)

	DATA.append(simulation_DATA)
	Topo.clear_routing_information()

	counter = counter + 1




'''
Write the results to a csv file
'''
print('Writing statistics to csv...')
csvfilename = './results/statistics__CAIDA'+dataset+'_sims'+str(nb_of_sims)+'_hijackType'+str(hijack_type)+'_test_hijacker'+'_.csv'
with open(csvfilename, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerows(DATA)
