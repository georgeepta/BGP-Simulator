import json


class NestedDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def read_hijack_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0

def write_evaluation_results(infection_accuracy_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(infection_accuracy_dict, json_file)

def infected_as_paths(paths_str, attacker_asn):
    infected_as_paths_list = []
    for path in paths_str.split(":"):
        path_list = path.split(" ")
        if path_list[-1] == attacker_asn:
            infected_as_paths_list.append(path_list)
    return infected_as_paths_list


def find_common_infected_ASes(hist_hijack_simulation_infected_nodes, hist_hijack_infected_as_paths_list):
    common_infected_ASes_list = []
    for path in hist_hijack_infected_as_paths_list:
        if path[0] in hist_hijack_simulation_infected_nodes.keys():
            common_infected_ASes_list.append(str(path[0]))
    print(common_infected_ASes_list)
    return common_infected_ASes_list


def compute_infection_accuracy_prefix_hijacks(hijack_id, accuracy_dict):
    hist_hijack_data = read_hijack_data("./evaluation_data/Historical-Hijacks/prefix-hijacks/"+str(hijack_id)+".json")
    for victim in hist_hijack_data["victims"]:
        for attacker in hist_hijack_data["attackers"]:
            hist_hijack_simulation_data = read_hijack_data("./evaluation_data/Historical-Hijacks/prefix-hijacks/"+str(hijack_id)+"_sim_"+victim+"_"+attacker+".json")
            if hist_hijack_simulation_data:
                hist_hijack_simulation_infected_nodes = hist_hijack_simulation_data[0]["after_hijack"]["dict_of_nodes_and_infected_paths_to_hijacker_prefix"]
                hist_hijack_infected_as_paths_list = infected_as_paths(hist_hijack_data["details"]["aspaths"], attacker)
                if hist_hijack_simulation_infected_nodes and hist_hijack_infected_as_paths_list:
                    common_infected_ASes_list = find_common_infected_ASes(hist_hijack_simulation_infected_nodes, hist_hijack_infected_as_paths_list)
                    infection_accuracy = len(common_infected_ASes_list) / len(hist_hijack_infected_as_paths_list)
                    print(str(hijack_id) + "  " + victim + "  " + attacker + "  " + str(infection_accuracy))
                    accuracy_dict["prefix_hijacks"][str(hijack_id)+"_sim_"+victim+"_"+attacker] = infection_accuracy


def compute_infection_accuracy_subprefix_hijacks(hijack_id, accuracy_dict):
    hist_hijack_data = read_hijack_data("./evaluation_data/Historical-Hijacks/subprefix-hijacks/"+str(hijack_id)+".json")
    for victim in hist_hijack_data["victims"]:
        for attacker in hist_hijack_data["attackers"]:
            hist_hijack_simulation_data = read_hijack_data("./evaluation_data/Historical-Hijacks/subprefix-hijacks/"+str(hijack_id)+"_sim_"+victim+"_"+attacker+".json")
            if hist_hijack_simulation_data:
                hist_hijack_simulation_infected_nodes = hist_hijack_simulation_data[0]["after_hijack"]["dict_of_nodes_and_infected_paths_to_hijacker_prefix"]
                hist_hijack_infected_as_paths_list = infected_as_paths(hist_hijack_data["details"]["sub_aspaths"], attacker)
                if hist_hijack_simulation_infected_nodes and hist_hijack_infected_as_paths_list:
                    common_infected_ASes_list = find_common_infected_ASes(hist_hijack_simulation_infected_nodes, hist_hijack_infected_as_paths_list)
                    infection_accuracy = len(common_infected_ASes_list) / len(hist_hijack_infected_as_paths_list)
                    print(str(hijack_id) + "  " + victim + "  " + attacker + "  " + str(infection_accuracy))
                    accuracy_dict["subprefix_hijacks"][str(hijack_id)+"_sim_"+victim+"_"+attacker] = infection_accuracy



if __name__ == '__main__':

    print("Simulator Accuracy per Prefix Hijack ...")

    print("Hijack ID | Victim ASN | Hijacker ASN | Accuracy")
    accuracy_dict = NestedDict()
    for hijack_id in list(range(1, 35, 1)):
        compute_infection_accuracy_prefix_hijacks(hijack_id, accuracy_dict)

    print("Simulator Accuracy per Subprefix Hijack ...")
    print("Hijack ID | Victim ASN | Hijacker ASN | Accuracy")
    for hijack_id in list(range(1, 31, 1)):
        compute_infection_accuracy_subprefix_hijacks(hijack_id, accuracy_dict)

    pref_hijack_accuracy_values = list(accuracy_dict["prefix_hijacks"].values())
    pref_hijack_avg_accuracy = sum(pref_hijack_accuracy_values) / len(pref_hijack_accuracy_values)
    accuracy_dict["prefix_hijacks"]["avg_accuracy"] = pref_hijack_avg_accuracy
    print("AVG accuracy Prefix Hijacks: " + str(pref_hijack_avg_accuracy))

    subpref_hijack_accuracy_values = list(accuracy_dict["subprefix_hijacks"].values())
    subpref_hijack_avg_accuracy = sum(subpref_hijack_accuracy_values) / len(subpref_hijack_accuracy_values)
    accuracy_dict["subprefix_hijacks"]["avg_accuracy"] = subpref_hijack_avg_accuracy
    print("AVG accuracy Subprefix Hijacks: " + str(subpref_hijack_avg_accuracy))

    print("Accuracy Summary Dict")
    print(accuracy_dict)
    write_evaluation_results(accuracy_dict, "accuracy_results.json")