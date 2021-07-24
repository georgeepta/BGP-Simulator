import json
import pytricia
import requests
from netaddr import IPNetwork
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

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
                    all_subnets.extend(list(prefix.subnet(prefix_len)))

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


def do_rov(endpoint_url, asn, prefix):
    url = endpoint_url + asn + "/" + prefix
    routinator_adapter = HTTPAdapter(max_retries=3)
    session = requests.Session()
    # Use `routinator_adapter` for all requests to endpoints that start with the endpoint_url argument
    session.mount(endpoint_url, routinator_adapter)
    try:
        response = session.get(url, timeout=3)
    except ConnectionError as ce:
        print(ce)
    except Timeout:
        print('The request timed out')
    else:
        print('The request did not time out')
        if response.status_code == 200:
            # Successful GET request
            print(response.json())
            return response.json()["validated_route"]["validity"]["state"]
        else:
            # HTTP Response not contains useful data for the ROV
            return response.status_code




if __name__ == '__main__':

    '''
    roas_path = '../datasets/RPKI-ROAs/test.json'
    ipv4_tree, ipv6_tree = create_roas_prefix_trees(roas_path)
    for prefix in ipv4_tree:
        print(prefix, ipv4_tree[prefix])

    for prefix in ipv6_tree:
        print(prefix, ipv6_tree[prefix])
    '''

    prefix = "1.0.0.0/24"
    asn = "13335"
    url = "http://localhost:9556/api/v1/validity/"

    state = do_rov(url, asn, prefix)
    print(state)
