import json
import pytricia
import random
import time
import csv
import requests
from netaddr import IPNetwork
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from mpipe import UnorderedStage, Pipeline, UnorderedWorker, Stage


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



class ProcessWorker(UnorderedWorker):

    def do_rov(self, endpoint_url, asn, prefix):
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

    def doTask(self, task):
        return self.do_rov(task["url"], task["asn"], task["prefix"])


class ProcessPrinter(UnorderedWorker):

    def update_progress_bar(self):
        return

    def doTask(self, sim_result):
        self.update_progress_bar()



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


def AsToOrgDict():

    AS_dict = {}
    Org_dict = {}

    file_path = '/home/george/UOC-CSD/MASTER/master_thesis/BGP-Simulator/datasets/AS-2-Orgs-mappings/20210701.as-org2info.jsonl'

    with open(file_path) as f:
        for line in f:
            data  = json.loads(line)
            if data["type"] == "ASN":
                ASN = data.pop("asn", None)
                if ASN not in AS_dict:
                    AS_dict[ASN] = data
            elif data["type"] == "Organization":
                Org = data.pop("organizationId", None)
                if Org not in Org_dict:
                    Org_dict[Org] = data
            else:
                #invalid line
                pass

    #ASN to Organization mapping
    for ASN in AS_dict:
        org_id = AS_dict[ASN]["organizationId"]
        if org_id in Org_dict.keys():
            org_data = Org_dict[org_id]
            AS_dict[ASN]["organizationDetails"] = org_data

    print(AS_dict)


def load_ROV_Deployment_monitor_data(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        asn_do_rov_list = []
        line_count=0
        for row in csv_reader:
            if line_count == 0:
                print(f'Columns names are {", ".join(row)}')
                line_count+=1
            else:
                print("ASN: "+row[0], "AS Name: "+row[1], "Certainty: "+row[2])
                if float(row[2]) >= 0.5:
                    asn_do_rov_list.append(int(row[0]))
                line_count+=1
        print(f'Processed: {line_count} lines.')
        print(asn_do_rov_list)
        return asn_do_rov_list

if __name__ == '__main__':

    '''
    roas_path = '../datasets/RPKI-ROAs/test.json'
    ipv4_tree, ipv6_tree = create_roas_prefix_trees(roas_path)
    for prefix in ipv4_tree:
        print(prefix, ipv4_tree[prefix])

    for prefix in ipv6_tree:
        print(prefix, ipv6_tree[prefix])
    

    rpki_validation = {("24409", "1.2.4.0/24") : "not-found",
                       ("38803", "1.2.4.0/24") : "invalid",
                       ("24151", "1.2.4.0/24"): "not-found",
                       ("24406", "1.2.4.0/24"): "not-found",
                       }

    print(rpki_validation[("24409", "1.2.4.0/24")])
    print(range(5))


    test_data = {"prefix": "1.0.0.0/24", "asn": "13335", "url": "http://localhost:9556/api/v1/validity/"}

    Stage1 = Stage(worker_class=ProcessWorker, size=5, do_stop_task=True, disable_result=False)
    Stage2 = Stage(worker_class=ProcessPrinter, do_stop_task=True, disable_result=True)
    ## Link the two workers in the same pipeline
    Stage1.link(Stage2)
    pipe = Pipeline(Stage1)


    start = time.time()
    for task in range(0,10000):
        pipe.put(test_data)
    #for task in range(0, 10000):
    #    do_rov(test_data["url"], test_data["asn"], test_data["prefix"])
    end = time.time()
    print(end - start)

    ## Term signal
    pipe.put(None)
    '''
    #AsToOrgDict()
    load_ROV_Deployment_monitor_data("../datasets/ROV-Deployment-Monitor/2020-08-31.csv")