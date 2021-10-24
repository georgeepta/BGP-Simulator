import json
import random


def read_ASRank_data(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def generate_rpki_rov_list(num_of_top_isp_rpki_adopters, rpki_adoption_propability, top_500_ASRank_ASNs):
    n_top_ISPs = int(num_of_top_isp_rpki_adopters/rpki_adoption_propability)
    set_of_n_top_ISPs = top_500_ASRank_ASNs["data"]["asns"]["edges"][0:n_top_ISPs]
    list_of_n_top_ASNs = []
    for item in set_of_n_top_ISPs:
        list_of_n_top_ASNs.append(int(item["node"]["asn"]))
    print(list_of_n_top_ASNs)
    print(random.sample(list_of_n_top_ASNs, num_of_top_isp_rpki_adopters))


if __name__ == '__main__':

    file_path = "../datasets/ASRank/top_500_ASNs.json"
    top_500_ASRank_ASNs = read_ASRank_data(file_path)

    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1]
    num_of_top_isp_rpki_adopters = list(range(0, 101, 10))
    generate_rpki_rov_list(10, 1, top_500_ASRank_ASNs)
