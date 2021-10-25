import json

def read_evaluation_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0


def compute_avg_impact(eval_data):
    impact_estimation_after_hijack_list = []
    for simulation_result in eval_data:
        impact_estimation_after_hijack_list.append(simulation_result["after_hijack"]["impact_estimation"])
    return sum(impact_estimation_after_hijack_list) / len(impact_estimation_after_hijack_list)

if __name__ == '__main__':
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1]
    num_of_top_isp_rpki_adopters = list(range(0, 101, 10))
    print("#### Evaluation ####")
    print("Number of Top RPKI adopters | RPKI Adoption Propability | Average Impact Estimation")
    for rpki_adopters_value in num_of_top_isp_rpki_adopters:
        for rpki_adoption_propability in rpki_adoption_propability_list:
            file_path = "./evaluation_data/prefix-hijacking-random/top-isps-"+str(rpki_adopters_value)+"/rpki-adoption-prop-"+str(rpki_adoption_propability)+".json"
            eval_data = read_evaluation_data(file_path)
            if eval_data:
                avg_impact_estimation_after_hijack = compute_avg_impact(eval_data)
                print(str(rpki_adopters_value) + "  " + str(rpki_adoption_propability) + "  " + str(avg_impact_estimation_after_hijack))
