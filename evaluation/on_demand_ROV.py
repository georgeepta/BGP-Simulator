import json
import requests
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter

class NestedDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def read_json_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0

def write_results_to_json(infection_accuracy_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(infection_accuracy_dict, json_file)

def do_rov(endpoint_url, origin_asn, prefix):
    url = endpoint_url + str(origin_asn) + "/" + prefix
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
        # print('The request did not time out')
        if response.status_code == 200:
            # Successful GET request
            # print(response.json())
            return response.json()["validated_route"]["validity"]["state"]
        else:
            # HTTP Response not contains useful data for the ROV
            return response.status_code


def start_ROV(asn_to_pfx_json, validator_url):
    ROV_results_dict = NestedDict()
    ROV_results_dict["valid"] = {}
    ROV_results_dict["invalid"] = {}
    ROV_results_dict["not-found"] = {}

    for ASN in asn_to_pfx_json:
        for pfx in asn_to_pfx_json[ASN]:
            validity_state = do_rov(validator_url, ASN, pfx)
            if ASN not in ROV_results_dict[validity_state]:
                ROV_results_dict[validity_state][ASN] = [pfx]
            else:
                ROV_results_dict[validity_state][ASN].append(pfx)

    return ROV_results_dict

if __name__ == '__main__':
    asn_to_pfx_json = read_json_data(r'evaluation_data/forth_ypourgeio_project/ASN_to_prefixes.json')
    '''
    We use the Rootinator tool to perform ROV. Rootinator performs ROV using 
    the most up-to-date set of Validated ROA Payloads (VRPs) provided by 
    the 5 RIRs. If the ROV result for an (IP-prefix, ASN) pair is "valid"
    it means that this ASN has a valid ROA for this prefix.
    '''
    ROV_results_dict = start_ROV(asn_to_pfx_json, 'http://localhost:9556/api/v1/validity/')
    write_results_to_json(ROV_results_dict, './evaluation_data/forth_ypourgeio_project/ROV_results.json')
    print(ROV_results_dict)