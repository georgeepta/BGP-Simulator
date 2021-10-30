import json

class NestedDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def read_evaluation_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0

def write_evaluation_results(evaluation_results_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(evaluation_results_dict, json_file)


def compute_avg_impact(eval_data):
    impact_estimation_after_hijack_list = []
    for simulation_result in eval_data:
        impact_estimation_after_hijack_list.append(simulation_result["after_hijack"]["impact_estimation"])
    return sum(impact_estimation_after_hijack_list) / len(impact_estimation_after_hijack_list)


def collateral_benefit_prefix_hijacking(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list, evaluation_results_dict):
    print("#### Collateral benefit Prefix Hijacking ####")
    print("Number of Top RPKI adopters | RPKI Adoption Propability | Average Impact Estimation")
    for rpki_adopters_value in num_of_top_isp_rpki_adopters:
        for rpki_adoption_propability in rpki_adoption_propability_list:
            file_path = "./evaluation_data/prefix-hijacking-random/top-isps-" + str(
                rpki_adopters_value) + "/rpki-adoption-prop-" + str(rpki_adoption_propability) + ".json"
            eval_data = read_evaluation_data(file_path)
            if eval_data:
                avg_impact_estimation_after_hijack = compute_avg_impact(eval_data)
                print(str(rpki_adopters_value) + "  " + str(rpki_adoption_propability) + "  " + str(
                    avg_impact_estimation_after_hijack))
                evaluation_results_dict["collateral_benefit"]["prefix_hijacking"][str(rpki_adopters_value)][str(rpki_adoption_propability)] = avg_impact_estimation_after_hijack


def collateral_benefit_subprefix_hijacking(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list, evaluation_results_dict):
    print("#### Collateral benefit Subprefix Hijacking ####")
    print("Number of Top RPKI adopters | RPKI Adoption Propability | Average Impact Estimation")
    for rpki_adopters_value in num_of_top_isp_rpki_adopters:
        for rpki_adoption_propability in rpki_adoption_propability_list:
            file_path = "./evaluation_data/subprefix-hijacking-random/top-isps-" + str(
                rpki_adopters_value) + "/rpki-adoption-prop-" + str(rpki_adoption_propability) + ".json"
            eval_data = read_evaluation_data(file_path)
            if eval_data:
                avg_impact_estimation_after_hijack = compute_avg_impact(eval_data)
                print(str(rpki_adopters_value) + "  " + str(rpki_adoption_propability) + "  " + str(
                    avg_impact_estimation_after_hijack))
                evaluation_results_dict["collateral_benefit"]["subprefix_hijacking"][str(rpki_adopters_value)][str(rpki_adoption_propability)] = avg_impact_estimation_after_hijack


def today_rov_status_other_random_prop_prefix_hijacking(other_random_prop_list, evaluation_results_dict):
    print("### Today ROV status + Other ASes (Prefix Hijacking) ###")
    print("RPKI Adoption Propability of other ASes | Average Impact Estimation")
    for prop_value in other_random_prop_list:
        file_path = "./evaluation_data/prefix-hijacking-random/today-rov-status/other-random-prop-" + str(prop_value) + ".json"
        eval_data = read_evaluation_data(file_path)
        if eval_data:
            avg_impact_estimation_after_hijack = compute_avg_impact(eval_data)
            print(str(prop_value) + "  " + str(avg_impact_estimation_after_hijack))
            evaluation_results_dict["today_rov_status_other_random_prop"]["prefix_hijacking"][str(prop_value)] = avg_impact_estimation_after_hijack


def today_rov_status_other_random_prop_subprefix_hijacking(other_random_prop_list, evaluation_results_dict):
    print("### Today ROV status + Other ASes (Subprefix Hijacking) ###")
    print("RPKI Adoption Propability of other ASes | Average Impact Estimation")
    for prop_value in other_random_prop_list:
        file_path = "./evaluation_data/subprefix-hijacking-random/today-rov-status/other-random-prop-" + str(prop_value) + ".json"
        eval_data = read_evaluation_data(file_path)
        if eval_data:
            avg_impact_estimation_after_hijack = compute_avg_impact(eval_data)
            print(str(prop_value) + "  " + str(avg_impact_estimation_after_hijack))
            evaluation_results_dict["today_rov_status_other_random_prop"]["subprefix_hijacking"][str(prop_value)] = avg_impact_estimation_after_hijack


if __name__ == '__main__':
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1.0]
    num_of_top_isp_rpki_adopters = list(range(0, 101, 10))
    other_random_prop_list = [v * 0.1 for v in range(0, 11, 1)]
    print("#### Evaluation Results ####")
    evaluation_results_dict = NestedDict()
    collateral_benefit_prefix_hijacking(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list, evaluation_results_dict)
    collateral_benefit_subprefix_hijacking(num_of_top_isp_rpki_adopters, rpki_adoption_propability_list, evaluation_results_dict)
    today_rov_status_other_random_prop_prefix_hijacking(other_random_prop_list, evaluation_results_dict)
    today_rov_status_other_random_prop_subprefix_hijacking(other_random_prop_list, evaluation_results_dict)
    write_evaluation_results(evaluation_results_dict, "evaluation_results.json")