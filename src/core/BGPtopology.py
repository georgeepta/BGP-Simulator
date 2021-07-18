#!/usr/bin/env python3
#
#
# Author: Georgios Eptaminitakis
# University of Crete, Greece
#
# E-mail: gepta@csd.uoc.gr
#
#
# This file is part of the BGPsimulator
#

import csv
import json
from src.core.BGPnode import BGPnode
from src.core.IXPNode import IXPNode
from collections import defaultdict
from collections import Iterable

class BGPtopology:
	''' 
	Class for network topology, where ASes are represented as single nodes (BGPnodes). 
	A BGPtopology contais
	        1. a list of the member nodes (objects of type BGPnode οr IXPNode).
	        2. (optionally) A list of the peer monitors (objects of type BGPnode).
	In this class, there exist methods related to (a) adding member nodes and links, (b) adding and hijacking IPprefixes, (c) obtaining various information from the member nodes of the topology.

	class variables: 
		(a) list_of_all_BGP_nodes:	dictionary (initially empty) - dictionary with (i) keys the ASNs of member nodes and (ii) values the objects of type BGPnode (corresponding to each member node)
	'''


	'''
	Contructor for object of the class BGPtopology. Creates the class variable "list_of_all_BGP_nodes" as an empty dictionary.
	'''
	def __init__(self):
		self.list_of_all_BGP_nodes = dict()
		self.list_of_all_monitors = set()
	
	'''
	Adds a node to the topology, i.e., to the dictionary "list_of_all_BGP_nodes".
	
	IF the given node does not exist in the "list_of_all_BGP_nodes" dictionary, 
	THEN add the node

	Input argument:
		(a) ASN: the ASN of the node to be added
	'''
	def add_node(self,ASN):
		if not self.has_node(ASN):
			self.list_of_all_BGP_nodes[ASN] = BGPnode(ASN,self)

	
	'''
	Remove node from topology.
	Not in use !!!

	TODO: need to implement BGP path withdrawals at the BGPPnode class first, and a destructor, and then can only define this method
	'''
	def remove_node(self,ASN):
		pass
		#if self.has_node(ASN):
		#	del self.list_of_all_BGP_nodes[ASN]


	'''
	Return a node (i.e. the BGPnode object) belonging to the topology.
	
	IF the given node exists in the "list_of_all_BGP_nodes" dictionary, 
	THEN return the node
	
	Input argument:
		(a) ASN: the ASN of the node to be returned

	Returns:
		A BGPnode object corresponding to the given ASN
	'''
	def get_node(self,ASN):
		return self.list_of_all_BGP_nodes[ASN]
		#if self.has_node(ASN):
		#	return self.list_of_all_BGP_nodes[ASN]

	
	'''
	Checks if the given node exists in the "list_of_all_BGP_nodes" dictionary.
	
	Input argument:
		(a) ASN: the ASN of the node to be checked

	Returns:
		TRUE if it exists, FALSE otherwise
	'''
	def has_node(self,ASN):
		if ASN in self.list_of_all_BGP_nodes:
			return True
		else:
			return False


	
	'''
	Adds a link in the topology between the two given nodes, and annotates the link according to the given peering type.

	IF the given nodes do not exist in the "list_of_all_BGP_nodes" dictionary, 
	THEN 	add them.
	IF a link between the two given nodes does not exist,
	THEN 	add ASN1 to ASN2's neighbors and ASN2 to ASN1's neighbors, and set the peering types according to the given type.
	
	Input arguments:
		(a) ASN1: the AS number of the first node
		(b) ASN2: the AS number of the second node
		(c) peering_type: an int (-1 or 0) that denotes the peering relation type between the two nodes; IF -1 then ASN2 is customer of ASN1, ELSE IF 0 then the nodes are peers
	'''
	def add_link(self,ASN1, ASN2,peering_type):
		if not self.has_node(ASN1):
			self.add_node(ASN1)
		if not self.has_node(ASN2):
			self.add_node(ASN2)
		if not self.has_link(ASN1,ASN2):
			if peering_type == -1:
				self.list_of_all_BGP_nodes[ASN1].add_ASneighbor(ASN2,'customer')
				self.list_of_all_BGP_nodes[ASN2].add_ASneighbor(ASN1,'provider')
			elif peering_type == 0:
				self.list_of_all_BGP_nodes[ASN1].add_ASneighbor(ASN2,'peer')
				self.list_of_all_BGP_nodes[ASN2].add_ASneighbor(ASN1,'peer')
			else:
				print('ERROR: Not valid peering relation')
		else:
			print('ERROR: a link already exists')


	def remove_link(self,ASN1, ASN2):
		if self.has_node(ASN1) and self.has_node(ASN2) and self.has_link(ASN1,ASN2):
			self.list_of_all_BGP_nodes[ASN1].remove_ASneighbor(ASN2)
			self.list_of_all_BGP_nodes[ASN2].remove_ASneighbor(ASN1)


	'''
	Checks if the given link exists in the topology.

	IF both nodes exist in the topology
	THEN 	IF node ASN1 has node ASN2 as neighbor AND node ASN2 has node ASN1 as neighbor
			THEN return TRUE

	
	Input arguments:
		(a) ASN1: the AS number of the first node
		(b) ASN2: the AS number of the second node

	Returns:
		TRUE if the link exists, FALSE otherwise
	'''
	def has_link(self,ASN1,ASN2):
		if self.has_node(ASN1) and self.has_node(ASN2):
			if self.get_node(ASN1).has_ASneighbor(ASN2) or self.get_node(ASN2).has_ASneighbor(ASN1):
				return True
		return False

	"""
	Returns the relation type of ASN1 to ASN2.
	Possible values: -1: customer, 0: peer, 1: provider or None if no such relation exists
	"""

	def get_link_type(self, ASN1, ASN2):
		if self.has_link(ASN1, ASN2):
			rel = self.get_node(ASN1).get_neighbor_relation(ASN2)
			if not (rel == 0 or rel == 1 or rel == -1): assert (False)
			return rel
		else:
			assert (False)

	'''
	Adds the given prefix to the given node.
	
	IF the node exists in the topology, 
	THEN add the prefix

	Input arguments:
		(a) ASN: the AS number of the node
		(b) IPprefix: the (owned) prefix to be added
	'''
	def add_prefix(self, ASN, IPprefix, forbidden_neighbors=None, neighbors_to_announce=None):
		if self.has_node(ASN):
			self.get_node(ASN).add_prefix(IPprefix,forbidden_neighbors=forbidden_neighbors, neighbors_to_announce = neighbors_to_announce)


	'''
	Hijack the given prefix from the given node with the given hijack type.
	
	IF the node exists in the topology, 
	THEN hijack the prefix

	Input arguments:
		(a) ASN: the AS number of the node
		(b) IPprefix: the (owned) prefix to be added
		(c) hijack_type: the type of the hijack attack
		(d) path (optional): Hijack using the given path
	Returns:
		The hijacker's announced path 
	'''
	def do_hijack(self, ASN, IPprefix, hijack_type = 0, path = None, neighbors_to_announce = None):
		assert (hijack_type or path), "Either provide a path to announce or specify the hijack type to craft the attack"

		if self.has_node(ASN):
			return self.get_node(ASN).do_hijack(IPprefix, hijack_type, path, neighbors_to_announce)


	'''
	Almost the same with the above function, but here we take 1 more argument --> the IPsubprefix
	'''
	def do_subprefix_hijack(self, ASN, IPprefix, IPsubprefix, hijack_type = 0, path = None, neighbors_to_announce = None):
		assert (hijack_type or path), "Either provide a path to announce or specify the hijack type to craft the attack"

		if self.has_node(ASN):
			return self.get_node(ASN).do_subprefix_hijack(IPprefix, IPsubprefix, hijack_type, path, neighbors_to_announce)



	'''
	Creates the nodes and links of the topology, based on the data of the given csv file.

	(Currently) it supports only files of the "CAIDA AS-relationship dataset" format (http://www.caida.org/data/active/as-relationships/)
	The format is:		ASN1|ASN2|peering_type|other_not_used_fields
				e.g., 	1|11537|0|bgp

	Input arguments:
		(a) file: a string with the name of the csv file to be read
		(b) type: a string denoting the format type of the csv file; default is 'CAIDA' (which is currently the only supported type)
	'''
	def load_topology_from_csv(self,file,type='CAIDA', asn_as_str=False):
		try:
			if type == 'CAIDA':
				with open(file, 'r') as csvfile:
					csvreader = csv.reader(csvfile,delimiter='|')
					counter = 0
					for row in csvreader:
						if row[0][0] is not '#':	# ignore lines starting with "#"
							counter += 1
							if asn_as_str:
								self.add_link(row[0],row[1],int(row[2]))
							else:
								self.add_link(int(row[0]),int(row[1]),int(row[2]))
		except IOError:
			print('ERROR: file not found')

		print("Topo: Loaded %s networks" % self.get_nb_nodes())
		print("Topo: Loaded %s node links" % counter)






	### methods to obtain (or print) various information from the member nodes of the topology ###
	# these methods could be used after an experiment, e.g., to  extract statistics for the number of hijacked paths, nodes, etc.



	'''
	Print some information for each node in the topology; see the respective method defined in the BGPnode class
	'''
	def print_info(self):
		for key,node in self.list_of_all_BGP_nodes.items():
			node.print_info()

	'''
	Returns the number of nodes in the topology, i.e., the length (number of keys) of the dictionary "list_of_all_BGP_nodes"
	'''
	def get_nb_nodes(self):
		return len(self.list_of_all_BGP_nodes)

	'''
	Returns the number of neighbors for each node of the topology in the form of a Dict AS: [nb_of_providers, nb_of_peers, nb_of_customers]
	'''
	def get_nb_neighbors(self):
		ASNneighbors = dict()
		for key, node in self.list_of_all_BGP_nodes.items():
			ASNneighbors[key] = node.get_nb_of_neighbors()
		return ASNneighbors

	'''
	Returns a list containing the ASNs (integers) of the nodes in the topology
	'''
	def get_all_nodes_ASNs(self):
		return list(self.list_of_all_BGP_nodes.keys())


	'''
	Returns a list containing the IP prefixes of all the nodes in the topology
	'''
	def get_list_of_prefixes(self):
		list_of_prefixes = {}
		for key,node in self.list_of_all_BGP_nodes.items():
			if node.get_prefixes():
				list_of_prefixes[key] = list(node.get_prefixes())
		return list_of_prefixes


	'''
	Returns a list containing the hijacked IP prefixes of all the nodes in the topology
	'''
	def get_list_of_hijacked_prefixes(self):
		list_of_hijacked_prefixes = []
		for key,node in self.list_of_all_BGP_nodes.items():
			if node.get_hijacked_prefixes():
				list_of_hijacked_prefixes.extend(node.get_hijacked_prefixes().keys())
		return list_of_hijacked_prefixes

	
	'''
	Returns a dictionary containing (a) as keys the hijacked IP prefixes of all the nodes in the topology and (b) as values the node that hijacked the prefix. 
	'''
	def get_list_of_hijacked_prefixes_and_hijackers(self):
		hijacked_prefixes_and_hijackers = {}
		for key,node in self.list_of_all_BGP_nodes.items():
			if node.get_hijacked_prefixes():
				for prefix in list(node.get_hijacked_prefixes().keys()):
					hijacked_prefixes_and_hijackers[prefix] = node.ASN
		return hijacked_prefixes_and_hijackers

	'''
	Returns True if the node is hijacking the given prefix.
	'''
	def has_hijacked_prefix(self, node, prefix):
		return self.list_of_all_BGP_nodes[node].has_hijacked_prefix(prefix)

	'''
	Returns the number of the (given) nodes that have a path to the given prefix (and, if any ASN is given, consider only paths originated by the given ASN)

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF an ASN is given
				THEN 	IF the path that the node has, is originated by the given ASN, 
						THEN increment the nb_of_nodes_with_path_to_prefix
				ELSE 	increment the nb_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) origin_ASN: 	the origin ASN for the paths (i.e., the first ASN in the path) to be considered; defount value is None (i.e., consider paths from any origin AS)
		(c) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		An integer denoting the number of nodes 
	'''
	def get_nb_of_nodes_with_path_to_prefix(self,IPprefix,origin_ASN = None, list_of_nodes=None):
		nb_of_nodes_with_path_to_prefix = 0

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key,node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				if origin_ASN:
					if node.paths.get(IPprefix)[-1] == origin_ASN:	# in case there is path, check the origin AS in the path
						nb_of_nodes_with_path_to_prefix += 1
				else:
					nb_of_nodes_with_path_to_prefix += 1

		return nb_of_nodes_with_path_to_prefix



	'''
	Returns the number of the (given) nodes that have a path (for the given prefix) that includes the hijacker ASN.

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF the path contains the given ASN
				THEN 	increment the nb_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) origin_ASN: 	the origin ASN for the paths (i.e., the first ASN in the path) to be considered; defount value is None (i.e., consider paths from any origin AS)
		(c) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		An integer denoting the number of nodes 
	'''
	def get_nb_of_nodes_with_hijacked_path_to_prefix(self,IPprefix,hijacker_ASN, list_of_nodes=None):
		nb_of_nodes_with_path_to_prefix = 0

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key,node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				if hijacker_ASN in node.paths.get(IPprefix):
					nb_of_nodes_with_path_to_prefix += 1

		return nb_of_nodes_with_path_to_prefix


	'''
	Returns the average path length that (the given) nodes have for the given prefix.

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF the path contains the given ASN
				THEN 	increment the nb_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		An number denoting the average path length (i.e., sum of path length over the number of nodes with path to prefix)
	'''
	def get_average_path_length(self,IPprefix,list_of_nodes=None):
		nb_of_nodes_with_path_to_prefix = 0
		sum_path_lengths = 0

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key,node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				sum_path_lengths = sum_path_lengths + len(node.paths.get(IPprefix))
				nb_of_nodes_with_path_to_prefix += 1

		if nb_of_nodes_with_path_to_prefix == 0:
			average_path_length = 0
		else:
			average_path_length = sum_path_lengths/nb_of_nodes_with_path_to_prefix

		return average_path_length



	'''
	Returns the set of the (given) nodes that have a path to the given prefix (and, if any ASN is given, consider only paths originated by the given ASN)

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF an ASN is given
				THEN 	IF the path that the node has, is originated by the given ASN,
						THEN increment the nb_of_nodes_with_path_to_prefix
				ELSE 	add node to the set_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) origin_ASN: 	the origin ASN for the paths (i.e., the first ASN in the path) to be considered; defount value is None (i.e., consider paths from any origin AS)
		(c) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		A set of ASNs
	'''
	def get_set_of_nodes_with_path_to_prefix(self,IPprefix,origin_ASN = None, list_of_nodes=None):
		set_of_nodes_with_path_to_prefix = set()

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key,node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				if origin_ASN:
					if node.paths.get(IPprefix)[-1] == origin_ASN:	# in case there is path, check the origin AS in the path
						set_of_nodes_with_path_to_prefix.add(node.ASN)
				else:
					set_of_nodes_with_path_to_prefix.add(node.ASN)

		return set_of_nodes_with_path_to_prefix

	'''
	Returns the set of the (given) nodes that have a path (for the given prefix) that includes the hijacker ASN.

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF the path contains the given ASN
				THEN 	add node to the set_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) hijacker_ASN: 	the hijacker ASN for the paths to be considered
		(c) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		A set of ASNs
	'''
	def get_set_of_nodes_with_hijacked_path_to_prefix(self,IPprefix,hijacker_ASN, list_of_nodes=None):
		set_of_nodes_with_path_to_prefix = set()
		assert (hijacker_ASN in self.list_of_all_BGP_nodes)

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		## added assert because this looks like a weird case
		assert (len(list_of_nodes_to_search) > 0)

		## Multiline src with unnecessary calls to get and add (far from optimal)
		#for key,node in list_of_nodes_to_search.items():
		#	if node.paths.get(IPprefix):
		#		if hijacker_ASN in node.paths.get(IPprefix):
		#			set_of_nodes_with_path_to_prefix.add(node.ASN)
		#return set_of_nodes_with_path_to_prefix

		## Replaced with optimized one line src (functionality same as above)
		return {node.ASN for node in list_of_nodes_to_search.values() if hijacker_ASN in node.paths.get(IPprefix, [])}


	''' *Custom function*
		Similar to the one above. Instead, It returns the set of the (given) nodes affected only by origin hijacking (type-0).
		Note: As a twist only the nodes poisoned by the hijacker are returned.
		Description: 
			see above
	'''

	def get_set_of_nodes_with_origin_hijacked_path_to_prefix(self, IPprefix, hijacker_ASN, list_of_nodes=None):
		set_of_nodes_with_path_to_prefix = set()
		assert (hijacker_ASN in self.list_of_all_BGP_nodes)

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes:
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		## Multiline src with unnecessary calls to get and add (far from optimal)
		# for key,node in list_of_nodes_to_search.items():
		#	if node.paths.get(IPprefix):
		#		if hijacker_ASN == node.paths.get(IPprefix)[-1]:
		#			#print(node.paths.get(IPprefix))
		#			set_of_nodes_with_path_to_prefix.add(node.ASN)
		# return set_of_nodes_with_path_to_prefix

		## Replaced with optimized one line src (functionality same as above)

		return {node.ASN for node in list_of_nodes_to_search.values() if (node.paths.get(IPprefix) and hijacker_ASN == node.paths[IPprefix][-1])}


	'''
	Returns the set of the (given) nodes that have a path (for the given prefix) that includes a specific edge (i.e., sequence of two ASNs).

	IF a list_of_nodes is given:
	THEN 	consider only the list of the given nodes (that exist in the topology)
	ELSE 	consider every node in the topology

	FOR all the considered nodes
		IF the node has a path to the prefix
		THEN	IF the path contains the given edge
				THEN 	add node to the set_of_nodes_with_path_to_prefix

	Input arguments:
		(a) IPprefix: 		the prefix for which paths to be considered
		(b) edge: 			a list with two elements: the ASes between which the edge exists
		(c) list_of_nodes: 	the list of nodes, which will be considered ; default value is None (i.e., consider all the nodes of the topology)

	Returns:
		A set of ASNs
	'''
	def get_set_of_nodes_with_specific_edge_to_prefix(self,IPprefix,edge, list_of_nodes=None, directed=False):
		set_of_nodes_with_path_to_prefix = set()

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key,node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				ASN1 = edge[0]
				ASN2 = edge[1]
				path = node.paths.get(IPprefix)
				if (ASN1 in path) and (ASN2 in path): # if both ASNs exists in the path ...
					if directed:
						if (path.index(ASN1) - path.index(ASN2)) == 1:	# ... and in sequence (i.e., form an edge from ASN1 to ASN2)
							set_of_nodes_with_path_to_prefix.add(node.ASN)
					else:
						if abs(path.index(ASN1) - path.index(ASN2)) == 1:	# ... and in sequence (i.e., form an edge)
							set_of_nodes_with_path_to_prefix.add(node.ASN)

		return set_of_nodes_with_path_to_prefix


	""" Custom Function
		Same as above but this time returns the set of nodes with a specific (sub)path to the prefix.
		The subpath has to appear in the same order as in the path variable (direction matters).
	"""

	def get_set_of_nodes_with_specific_path_to_prefix(self, IPprefix, subpath, list_of_nodes=None):
		set_of_nodes_with_path_to_prefix = set()
		subpathlen = len(subpath)

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes:
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		## quickly check if a node's best path includes the subpath
		## First, find the indexes of all ASes that are equal with the first AS in the subpath
		## Then, quickly compare if the path that starts from those indexes is equal to subpath
		for node in list_of_nodes_to_search.values():
			node_path = node.paths.get(IPprefix)
			if node_path:
				indices = [index for index, ASN in enumerate(node_path) if ASN == subpath[0]]
				has_subpath = [i for i in indices if node_path[i:i + subpathlen] == subpath]
				if has_subpath: set_of_nodes_with_path_to_prefix.add(node.ASN)

		return set_of_nodes_with_path_to_prefix


	def get_nb_of_nodes_with_specific_edge_to_prefix(self,IPprefix,edge,list_of_nodes=None, directed=False):
			return len(self.get_set_of_nodes_with_specific_edge_to_prefix(IPprefix,edge,list_of_nodes,directed))


	""" Custom Function
		Operates like the similar function above. 
		Instead of returning the nodes having the specific edge to the prefix it returns the best paths of those nodes 
		that include the edge. Thus, this list_of_nodes to check is now required.

		Input arguments:
			(a) IPprefix: 		the prefix for which paths to be considered
			(b) edge: 			a list with two elements: the ASes between which the edge exists
			(c) list_of_nodes: 	the list of nodes, which will be considered. 
		Returns:
			A list of paths one for each node in the list_of_nodes. 
			If a node didnt have an edge the the corresponding path will be empty
	"""

	def get_paths_of_nodes_with_specific_edge_to_prefix(self, IPprefix, edge, list_of_nodes=[], directed=False):
		list_of_paths_with_edge_to_prefix = dict()

		assert (list_of_nodes), "no nodes provided"

		if list_of_nodes:
			list_of_nodes_to_search = {}
			for key in list_of_nodes:
				if key in self.list_of_all_BGP_nodes.keys():
					list_of_nodes_to_search[key] = self.list_of_all_BGP_nodes[key]
		else:
			list_of_nodes_to_search = self.list_of_all_BGP_nodes

		for key, node in list_of_nodes_to_search.items():
			if node.paths.get(IPprefix):
				ASN1 = edge[0]
				ASN2 = edge[1]
				path = node.paths.get(IPprefix)
				if (ASN1 in path) and (ASN2 in path):  # if both ASNs exists in the path ...
					if directed:
						if (path.index(ASN1) - path.index(ASN2)) == 1:  # ... and in sequence (i.e., form an edge from ASN1 to ASN2)
							list_of_paths_with_edge_to_prefix[key] = path
							continue
					else:
						if abs(path.index(ASN1) - path.index(ASN2)) == 1:  # ... and in sequence (i.e., form an edge)
							list_of_paths_with_edge_to_prefix[key] = path
							continue

			list_of_paths_with_edge_to_prefix[key] = []

		return list_of_paths_with_edge_to_prefix


	""" Custom Function
		Returns the best paths of all nodes to the specified prefix.
		Note: For hijacked prefixes, the fake path may be returned (depends on whether the node is poisoned or not)
		Inputs
			a) An already announced prefix. 
			b) The list of nodes to consider. IF None consider all nodes.
		outputs
			a) dictionary of nodes and paths to the specified prefix. For nodes with no path to the prefix the correspondind entry is None
	"""

	def Get_path_to_prefix(self, IPprefix, nodes_to_consider=None):
		if nodes_to_consider is None: nodes_to_consider = self.list_of_all_BGP_nodes

		path_to_prefix = dict()
		for node in nodes_to_consider:
			path_to_prefix[node] = self.list_of_all_BGP_nodes[node].get_path(IPprefix)
			## added the below line to return shallow copies of the paths
			if isinstance(path_to_prefix[node], list): path_to_prefix[node] = list(path_to_prefix[node])

		return path_to_prefix


	""" Custom Function
		For a non-hijacked prefix:
			For a given AS and one of its prefixes returns the best paths as observed by the monitors for that prefix.
			To do this, the edge of the given AS with its neighbors is used.
		For a hijacked prefix the result depends on the poisoning done by the hijacker
			IF the hijacker is not poisoning using the edge <ASN, ASN_nbor>  Then returns the best valid paths
			IF the hijacker is poisoning using the edge <ASN, ASN_nbor>  Then poisoned paths may also be returned
		Inputs:
			(a) The ASN whose paths will be returned
			(b) The prefix of that ASN
			(c) (optional) The neighbors (providers) to be considered. Only best paths from those neighbors (providers) will be considered.
			               Default value: consider all neighbors
			Note that if the same prefix has been announced to two providers then only one (per monitor) will have a best path.

		Returns
			(a) a dictionary of the best paths per monitor
				Format: paths[monitor_AS] = paths
			    OR if nbors_to_consider is provided, a dictionary of the best paths per monitor as seen by each neighbor. 
			    Format paths[nbor_AS][monitor_AS] = paths
			    Note monitor paths can be empty. Especially if a monitor is not accessible from a neighbor
	"""

	def get_node_best_paths_seen_by_monitors(self, ASN, prefix, nbors_to_consider=[]):

		if ASN not in self.list_of_all_BGP_nodes:              assert (False), "BGP node not found"
		if prefix not in self.list_of_all_BGP_nodes[ASN].paths: assert (False), "ASN does not have such prefix"

		care_for_neighbors = False
		if not nbors_to_consider:
			nbors_to_consider = self.get_node_neighbors(ASN)
		else:
			care_for_neighbors = True

		paths_seen_by_monitors = dict()
		monitors_to_consider = list(self.list_of_all_monitors)
		for nbor in nbors_to_consider:
			edge_to_consider = [ASN, nbor]
			paths = self.get_paths_of_nodes_with_specific_edge_to_prefix(prefix, edge_to_consider, monitors_to_consider, directed=True)

			if care_for_neighbors:
				paths_seen_by_monitors[nbor] = paths
			else:
				## It is not possible for an AS (either monitor or not) to have two best paths at the same time.
				# paths_seen_by_monitors.update(paths)
				for mon_as in paths:
					# assert(mon_as not in paths_seen_by_monitors), "mon_as %s \n paths_seen_by_monitors %s " %(mon_as, paths_seen_by_monitors)
					if mon_as not in paths_seen_by_monitors or len(paths[mon_as]) != 0:
						assert (mon_as not in paths_seen_by_monitors or len(paths_seen_by_monitors[mon_as]) == 0), "mon_as %s\n paths_seen_by_monitors %s \n %s ok" % (mon_as, paths_seen_by_monitors[mon_as], paths[mon_as])
						paths_seen_by_monitors[mon_as] = paths[mon_as]

			for monitor, mon_path in paths.items():
				## Sanity checks
				if len(mon_path) == 0: continue
				assert (mon_path[0] in self.get_node_neighbors(monitor))
				assert (mon_path[-1] == ASN)
				assert (mon_path[-2] == nbor)

		return paths_seen_by_monitors


	""" * Custom Function *
		For a given AS node returns all of its neighbors that offer a path to the specified prefix.
		Limitations:
			The function may have a different output depending on when it is used; before or after the hijack.
			IF used before, then return the neighbors that offer a valid path.
			IF used after, then return the neighbors that offer both a valid and a poisoned path introduced by the hijacker.
				NOTE: if ASN = Hijacker_ASN and IPprefix = Hijacked_prefix output is UNDEFINED

		Input arguements:
			a) The ASN which will be checked 
			b) The prefix of which the paths will be queried.
			c) (optional) A safety flag to void unintended use. Please Read description
		"""

	def get_neighbors_of_node_with_path_to_prefix(self, ASN, IPprefix, prefix_is_hijacked=False):
		# if ASN in self.list_of_all_BGP_nodes:
		if not prefix_is_hijacked:
			hijacked_prefixes = self.get_list_of_hijacked_prefixes()
			assert (IPprefix not in hijacked_prefixes), "Change Prefix is hijacked flag to True"

		node = self.list_of_all_BGP_nodes[ASN]
		return node.get_neighbors_with_path_to_prefix(IPprefix)


	""" * Custom Function *
	Given a node's ASN returns number of its neighbors. For a multiple AS input, refer to get_nb_neighbors function.
	"""
	def get_node_neighbors_nb(self, ASN):
		nb_of_providers, nb_of_peers, nb_of_customers = self.list_of_all_BGP_nodes[ASN].get_nb_of_neighbors()
		return nb_of_providers + nb_of_peers + nb_of_customers

	""" * Custom Function *
	Given a node's ASN returns a unified list of all of its neighbors independent of type (i.e customer, peer, provider).
	"""

	def get_node_neighbors(self, ASN):
		return self.list_of_all_BGP_nodes[ASN].ASneighbors.keys()
		## Old src (slower) follows
		# ASN_nbors = set()
		# nbor_by_type = self.list_of_all_BGP_nodes[ASN].get_neighbors()	## dict of the form: {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}
		# for nbor_type in nbor_by_type: ASN_nbors.update( nbor_by_type[nbor_type] )
		# return ASN_nbors


	""" * Custom Function *
		Given a node's ASN returns the neighbor dictionary in the form  {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}
		Useful when the type of nbor connection matters. If not use the "get_node_neighbors" function
	"""
	def get_node_neighbors_by_type(self, ASN):
		return self.list_of_all_BGP_nodes[ASN].get_neighbors()  ## dict of the form: {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}


	""" * Custom Function *
		Given an AS and one of its neighbors, returns the conn-type to the neighbor (customers, providers or peers)
		Notes: This is similar to "get_link_type" function but without verifying that the nbor exists
	"""
	def get_node_neighbor_type(self, ASN, nborAS):
		nbor_rel = self.list_of_all_BGP_nodes[ASN].get_neighbor_relation(nborAS)  ## -1: customer, 0: peer, 1: provider
		if nbor_rel == -1: return "customers"
		elif nbor_rel == 1: return "providers"
		elif nbor_rel == 0: return "peers"
		else: assert (False), "Unknown neighbor conn-type"


	""" * Custom Function *
		Given a node's ASN returns the list of its providers and peers
	"""
	def get_node_providers_and_peers(self, ASN):
		ASN_nbors = set()
		nbor_by_type = self.list_of_all_BGP_nodes[ASN].get_neighbors()  ## dict of the form: {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}
		ASN_nbors.update(nbor_by_type["providers"])
		ASN_nbors.update(nbor_by_type["peers"])

		return ASN_nbors


	""" * Custom Function *
		Given a node's ASN returns the list of its customers
	"""
	def get_node_customers(self, ASN):
		ASN_nbors = set()
		nbor_by_type = self.list_of_all_BGP_nodes[ASN].get_neighbors()  ## dict of the form: {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}
		ASN_nbors.update(nbor_by_type["customers"])

		return ASN_nbors


	""" * Custom Function *
		Given a node's ASN returns the list of its providers
	"""
	def get_node_providers(self, ASN):
		ASN_nbors = set()
		nbor_by_type = self.list_of_all_BGP_nodes[ASN].get_neighbors()  ## dict of the form: {'providers' : list_of_providers, 'peers' : list_of_peers, 'customers' : list_of_customers}
		ASN_nbors.update(nbor_by_type["providers"])

		return ASN_nbors


	""" * Custom Function *
		For the specified node check which nbor is more tie-prefered.
		Returns: True if nbor1 more tied-prefered than nbor 2, else False
	"""
	def has_highest_tie_preference(self, node_ASN, nbor1, nbor2):
		return self.list_of_all_BGP_nodes[node_ASN].has_highest_tie_prefererence(nbor1, nbor2)


	""" * Custom Function *
		Checks whether the hijacker maintains a path towards the victim network or not.
		A path is maintained, if no node along the path has been poisoned. 

		Inputs:
			a) the hijacker ASN
			b) the victim   ASN
			c) the hijacked prefix
			d) the specific nbor to check (optional). If not provided, checks all nbors.
		Returns:
			a) if nbor has been specified, the interception path provided by that nbor if it is still avalable. Else, an empty list
			   if nbor was not  specified, the first interception path discovered that is still available. Else an empty list
	"""
	def interception_is_possible(self, hijackerAS, victimAS, IPprefix, nbor_to_check=None):
		hijack_node = self.list_of_all_BGP_nodes[hijackerAS]

		## for each path the hijacker still maintains towards the victim
		## verify that the path is real; check all AS nodes along the path except the origin.
		## If the best path of every AS along the remains unchanged then, the hijacker maintains a valid path.

		if nbor_to_check is None:
			paths_to_victim = hijack_node.all_paths[IPprefix].values()
		else:
			if nbor_to_check not in hijack_node.all_paths[IPprefix]: assert (False), "nbor not found in hijacker_nbors"
			paths_to_victim = [hijack_node.all_paths[IPprefix][nbor_to_check]]

		for path in paths_to_victim:
			assert (victimAS == path[-1])
			poisoned_ASes_in_path = self.get_set_of_nodes_with_hijacked_path_to_prefix(IPprefix, hijackerAS,list_of_nodes=path[:-1])  # checks the whole path at once.
			if len(poisoned_ASes_in_path) == 0: return path

		return []



	'''
	Writes some main information about the hijacked prefixes in the given csv file.

	(Currently) it writes to the given csv file a row per hijacked prefix.
	The format is:		nb_of_nodes_with_path_to_prefix,nb_of_nodes_with_hijacked_path_to_prefix(,nb_of_nodes_from_the_given_list_with_path_to_prefix,nb_of_nodes_from_the_given_list_with_hijacked_path_to_prefix)
				e.g., 	10,5,4,1

	Input arguments:
		(a) csv_filename: a string with the name of the csv file to be written
		(b) list_of_nodes: 	the list of the specific nodes, which will be considered; default is None
	'''
	def write_hijacking_data_to_csv(self,csv_filename,list_of_nodes=None):
		with open(csv_filename, 'w') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',')
			for prefix,hijacker in self.get_list_of_hijacked_prefixes_and_hijackers().items():
				#print('writing statistics to csv ... '+str(100*i/nb_of_sims)+'%\r',end='')
				DATA = []
				DATA.append(self.get_nb_of_nodes_with_path_to_prefix(prefix))
				DATA.append(self.get_nb_of_nodes_with_hijacked_path_to_prefix(prefix,hijacker))
				if list_of_nodes:
					DATA.append(self.get_nb_of_nodes_with_path_to_prefix(prefix,None,list_of_nodes))
					DATA.append(self.get_nb_of_nodes_with_hijacked_path_to_prefix(prefix,hijacker,list_of_nodes))
				spamwriter.writerow(DATA)

	'''
		Loads IXP nodes from Caida's dataset. Each IXP node contains the following information:
			a) IXP_id
			b) IXP_name
			c) IXP_country
			d) IXP_city
			e) IXP_region
			f) IXP_connected_members
	'''
	def load_ixps_from_json(self, ixp_file, ix_as_file):

		from ujson import loads
		self.list_of_all_IXP_nodes = {}

		## First, Load info that identifies each IXP (& Verify that there are no duplicates)
		with open(ixp_file, 'r') as fp:
			for line in fp:
				if line.split()[0] == "#": continue
				ixp_info = loads(line)
				ixp_id   = int(ixp_info['ix_id'])
				assert(ixp_id not in self.list_of_all_IXP_nodes)
				self.list_of_all_IXP_nodes[ixp_id] = IXPNode(ixp_info)

		print("Topo: Loaded %s IXP networks" %len(self.list_of_all_IXP_nodes))

		## Second, Load member info about the ASes connected each IXP.
		self.load_ixp_members_from_json(ix_as_file)


	'''
	Populates the IXP node membership info.
	For consistency reasons, ASes missing from the original topology will be ignored.
	'''

	def load_ixp_members_from_json(self, ix_as_file):

		from ujson import loads
		ignored_members = set()
		count_members = 0

		with open(ix_as_file, 'r') as fp:
			for ASline in fp:
				if ASline.split()[0] == "#": continue
				ASline = loads(ASline)
				ix_id = int(ASline["ix_id"])
				asn = int(ASline["asn"])

				assert (ix_id in self.list_of_all_IXP_nodes)
				assert (asn not in self.list_of_all_IXP_nodes[ix_id].ASN_members())

				if asn in self.list_of_all_BGP_nodes:
					self.list_of_all_IXP_nodes[ix_id].add_ASN_member(asn)
					count_members += 1
				else:
					ignored_members.add(asn)

		print("Topo: Added    %s ASes to IXPs" % count_members)
		print("Topo: Ignored  %s IXP ASes missing from original topo" % len(ignored_members))

	'''
	Add the extra IXP-based p2p links. Requires a file with this knowledge. If the file is missing refer to "add_extra_p2p_custom_links"
	'''
	def add_extra_p2p_links_from_json(self, json_filename):
		with open(json_filename, 'r') as jsonfile:
			all_asn_asn_ixp_tuples = json.load(jsonfile)

		i_asn  = 0
		i_link = 0
		for t in all_asn_asn_ixp_tuples:
			if not self.has_node(t[0]) or not self.has_node(t[1]):
				i_asn += 1

			if not self.has_link(t[0],t[1]):
				self.add_link(t[0], t[1], 0)
				i_link += 1

		print ("%i new p2p links added in total" % (i_link))
		print ("%i new ASNs added in total because of the extra p2p links" % (i_asn))

	'''
	In lack of IXP p2p information, assign every member of the same IXP in a p2p relation.
	IF a relation between the two connected members already exists in the topology: 
		Then instead keep the existing relation intact.
	'''

	def add_extra_p2p_custom_links(self):
		exist_already_links = set()
		established_links = set()
		for ixp_id in self.list_of_all_IXP_nodes:
			ixp_members = list(self.list_of_all_IXP_nodes[ixp_id].ASN_members())

			for index, ixp_member in enumerate(ixp_members):
				rest_members = ixp_members[index + 1:]
				for other_member in rest_members:
					assert (ixp_member != other_member)
					str_link = "%s_%s" % (ixp_member, other_member) if ixp_member > other_member else "%s_%s" % (
					other_member, ixp_member)
					if self.has_link(ixp_member, other_member):  ## Fixes both directions
						"""
                        Add the src below instead to replace instead existing policies to p2p.
                        if self.get_link_type(ixp_member, other_member) == 0: continue
                        else: self.remove_link(ixp_member, other_member)
                        self.add_link(ixp_member, other_member, 0)
                        """
						if str_link not in established_links: exist_already_links.add(str_link)
					else:
						self.add_link(ixp_member, other_member, 0)
						established_links.add(str_link)

		## Debug: verify that everyone is connected to everyone
		for ixp_id in self.list_of_all_IXP_nodes:
			ixp_members = self.list_of_all_IXP_nodes[ixp_id].ASN_members()
			for ixp_member in ixp_members:
				rest_members = set(ixp_members)
				rest_members.remove(ixp_member)
				for other_member in rest_members:
					assert (self.has_link(ixp_member, other_member))

		print("Topo: Established  %d new connections via IXPs" % len(established_links))
		print("Topo: Not altering %d old connections that exist in the topology" % len(exist_already_links))

	'''
	Implement remote peering with a certain IXP
	'''
	def peer_remotely_with_IXP(self, ASN, ixp_id):
		ixp_members = self.list_of_all_IXP_nodes[ixp_id].members

		#add the remote peer as a new IXP member
		self.list_of_all_IXP_nodes[ixp_id].add_ASN_member(ASN)

		#add the remote p2p links with all current open IXP members
		i = 0
		for member in ixp_members:
			if not self.has_link(ASN,member):
				self.add_link(ASN, member, 0)
				i += 1


		#print("%i new p2p links added due to remote peering of ASN %i with IXP %s!" %(i, ASN, ixp_id))

	'''
	Returns a list containing the IXPs (integers)
	'''
	def get_all_nodes_IXPs(self):
		return list(self.list_of_all_IXP_nodes.keys())


	'''
	Clears the routing information of all nodes in topology.
	'''
	def clear_routing_information(self,list_of_nodes=None):
		if not list_of_nodes:
			list_of_nodes = self.get_all_nodes_ASNs()
		for ASN in list_of_nodes:
			self.get_node(ASN).clear_routing_tables()
