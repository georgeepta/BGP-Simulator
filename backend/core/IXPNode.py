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

from pprint import pprint as pp

class IXPNode:
    '''
    Class for IXP nodes

    Class variables:
        (a) ix_id               : integer,example : 986,
        (b) name                : string, example : 'MidWest-IX',
        (c) members             : list of ASNs that are members with this IXP (under open policy)
        (d) country             : string, example : 'US',
        (e) region              : string, example : 'North America',
        (d) city                : string, example : 'Indianapolis, Indiana',


    Input arguments:
		raw_dict: dictionary with all the ixp related data from peeringdb
    '''

    def __init__(self, ixp_info):
        self.ix_id = int(ixp_info['ix_id'])
        self.name = ixp_info['name']
        self.members = set()
        if 'country' in ixp_info: self.country = ixp_info['country']
        if 'region' in ixp_info: self.region = ixp_info['region']
        if 'city' in ixp_info: self.city = ixp_info['city']

    def add_ASN_member(self, ASN):
        self.members.add(ASN)

    def remove_ASN_member(self, ASN):
        self.members.remove(ASN)

    def ASN_members(self):
        return self.members

    ### methods for	printing information ###
    def print_info(self):
        print('***IXP***: '     +str(self.ix_id))
        print('ID = '           + str(self.ix_id))
        print('Name = '         + str(self.name))
        print('City = '         + str(self.city))
        print('Country = '      + str(self.country))
        print('Members = ')
        pp(self.members)
        print(' ')
