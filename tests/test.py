import json

import netaddr
import pytricia
from netaddr import IPNetwork


def create_roas_prefix_trees(file_path):

    with open(file_path, 'r') as fp:
        data = json.load(fp)
        ipv4_pyt = pytricia.PyTricia()
        ipv6_pyt = pytricia.PyTricia(128)

        for roa in data["roas"]:
            prefix = IPNetwork(roa['prefix'])
            all_subnets = [prefix]
            min_length = prefix.prefixlen
            if roa['maxLength'] != "" and roa['maxLength'] > min_length:
                for prefix_len in range(min_length + 1, roa['maxLength'] + 1):
                    all_subnets = all_subnets + list(prefix.subnet(prefix_len))

            if prefix.version == 4:  # do the insertions in the IPv4 prefix tree
                for subnet in all_subnets:
                    if ipv4_pyt.has_key(str(subnet)):  # if the prefix exist in tree
                        if roa['asn'] not in ipv4_pyt.get(
                                str(subnet)):  # and the origin asn not exist in the list associated with the prefix
                            ipv4_pyt[str(subnet)].append(roa['asn'])  # insert it in the list
                    else:
                        ipv4_pyt[str(subnet)] = [roa['asn']]  # if the prefix not exist in tree, insert it and create a list containing the origin AS

            elif prefix.version == 6:  # do the insertions in the IPv6 prefix tree
                for subnet in all_subnets:
                    if ipv6_pyt.has_key(str(subnet)):  # if the prefix exist in tree
                        if roa['asn'] not in ipv6_pyt.get(
                                str(subnet)):  # and the origin asn not exist in the list associated with the prefix
                            ipv6_pyt[str(subnet)].append(roa['asn'])  # insert it in the list
                    else:
                        ipv6_pyt[str(subnet)] = [roa['asn']]  # if the prefix not exist in tree, insert it and create a list containing the origin AS

            else:
                assert (False), "Invalid prefix version it must be IPv4 orIPv6"

        return ipv4_pyt, ipv6_pyt


if __name__ == '__main__':

    roas_path = '../datasets/RPKI-ROAs/test.json'
    ipv4_tree, ipv6_tree = create_roas_prefix_trees(roas_path)

    for prefix in ipv4_tree:
        print(prefix, ipv4_tree[prefix])

    for prefix in ipv6_tree:
        print(prefix, ipv6_tree[prefix])
