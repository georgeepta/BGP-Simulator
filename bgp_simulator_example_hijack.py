#!/usr/bin/env python3
#
#
# Author: Pavlos Sermpezis
# Institute of Computer Science, Foundation for Research and Technology - Hellas (FORTH), Greece
#
# E-mail: sermpezis@ics.forth.gr
#
#


from BGPtopology import BGPtopology
#import time
import random
import sys
import csv





'''
A script that (i) does a number of hijacking simulations with anycast mitigation, (ii) saves the results (in pkl type), and (iii) write some main information from the results to a csv file.

Input (command-line) arguments:
	(a) nb_of_sims: an integer denoting the number of experiment runs (repetitions) of the simulation
	(b) hijack_type: an integer in {0,1,2,3,...} denoting the type of hijacking attack, with 0 = origin AS attack , 1 = 1st hop attack, etc.
	(c) dataset: an integer of type yyyymmdd denoting the dataset from which the topology will be loaded
	(d) max_nb_anycast_ASes: an integer denoting the maximum number of anycast ASes to be used for hijack mitigation

Topologies are stored in the "../CAIDA AS-graph/serial-2/" folder.

The csv is formatted as follows:
'''



'''
read the input arguments; if incorrect arguments, exit
'''  
if len(sys.argv) is 5:
	nb_of_sims = int(sys.argv[1]) #1000
	hijack_type = int(sys.argv[2]) # 0 or 1 or 2 or ...
	dataset = sys.argv[3] # 20160901
	max_nb_anycast_ASes = int(sys.argv[4]) #20	
else:
	sys.exit("Incorrent arguments. Arguments should be {nb_of_sims, hijack_type, dataset_id, max_nb_anycast_ASes}")



'''
load and create topology
'''
print('Loading topology...')
Topo = BGPtopology()
Topo.load_topology_from_csv('./CAIDA AS-graph/serial-2/'+dataset+'.as-rel2.txt')


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
for i in range(nb_of_sims):
	print('simulation step: '+str(100*simulation_step/nb_of_sims)+'%\r',end='')
	simulation_step += 1

	# randomly select victim, hijacker, anycasters (for mitigation)
	r = random.sample(list_of_ASNs,2+max_nb_anycast_ASes)
	legitimate_AS = r[0]
	hijacker_AS = r[1]
	anycast_ASes = r[2:]
	prefix = simulation_step

	# do the legitimate announcement from the victim
	Topo.add_prefix(legitimate_AS,prefix)
	simulation_DATA = []	# "simulation_DATA" will contain the data to be saved as the output of the simulation
	simulation_DATA.append(Topo.get_nb_of_nodes_with_path_to_prefix(prefix))
	simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(prefix,hijacker_AS))

	# do the hijack from the hijacker
	Topo.do_hijack(hijacker_AS,prefix,hijack_type)
	simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(prefix,hijacker_AS))

	# do the mitigation by anycasting the prefix from helper ASes (assuming they will attract traffic and then tunnel it to the victim)
	for anycast_AS in anycast_ASes:
		Topo.add_prefix(anycast_AS,prefix)
	simulation_DATA.append(Topo.get_nb_of_nodes_with_hijacked_path_to_prefix(prefix,hijacker_AS))

	simulation_DATA.append(hijacker_AS)
	simulation_DATA.append(legitimate_AS)

	DATA.append(simulation_DATA)
	Topo.clear_routing_information()




'''
Write the results to a csv file
'''
print('Writing statistics to csv...')
csvfilename = './statistics__CAIDA'+dataset+'_sims'+str(nb_of_sims)+'_hijackType'+str(hijack_type)+'_test_hijacker'+'_.csv'
with open(csvfilename, 'w') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerows(DATA)
