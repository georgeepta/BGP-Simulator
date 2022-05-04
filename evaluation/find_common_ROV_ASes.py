import csv
import json

class NestedDict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def write_results_to_json(ROV_ASes_dict_results, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(ROV_ASes_dict_results, json_file)


def load_ROV_Deployment_monitor_data(file_path):
    asn_do_rov_list = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Columns names are {", ".join(row)}')
                line_count += 1
            else:
                print("ASN: " + row[0], "AS Name: " + row[1], "Certainty: " + row[2])
                if float(row[2]) >= 0.0:
                    asn_do_rov_list.append(int(row[0]))
                line_count += 1
        print(f'Processed: {line_count} lines.')
        print(asn_do_rov_list)
    return asn_do_rov_list


def load_ROV_Active_Measurements_TMA_data(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
        # use the Total Unique ROV (Fully+Partially filtering) result
        asn_do_rov_list = [int(item) for item in data["2"][129]]
        print(asn_do_rov_list)
        return asn_do_rov_list


def load_Is_BGP_Safe_Yet_Cloudflare_ASes(file_path):
    rov_ASes_list = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Columns names are {", ".join(row)}')
                line_count += 1
            else:
                print("AS Name: " + row[0], "type: " + row[1], "details: " + row[2], "status: " + row[3], "ASN: " + row[4], "rank: " + row[5])
                if row[3] not in ["unsafe"]:
                    rov_ASes_list.append(int(row[4]))
                line_count += 1
        print(f'Processed: {line_count} lines.')
        print(rov_ASes_list)
    return rov_ASes_list


def find_common_union_ROV_ASes_Active_Measurements_TMA_paper_2021_Rodday_data(datasets_path, dataset_dates_list, ROV_ASes_dict_results):
    all_ROV_ASes_list_of_lists = []
    for date in dataset_dates_list:
        all_ROV_ASes_list_of_lists.append(load_ROV_Active_Measurements_TMA_data(datasets_path + date + "_resultset_asns.json"))

    union_ROV_ASes = list(set([item for sublist in all_ROV_ASes_list_of_lists for item in sublist]))
    common_ROV_ASes = list(set(all_ROV_ASes_list_of_lists[0]).intersection(*all_ROV_ASes_list_of_lists))

    ROV_ASes_dict_results["TMA_paper_2021_Rodday"]["union_ROV_ASes_of_all_measurements_list"] = union_ROV_ASes
    ROV_ASes_dict_results["TMA_paper_2021_Rodday"]["union_ROV_ASes_of_all_measurements_count"] = len(union_ROV_ASes)
    ROV_ASes_dict_results["TMA_paper_2021_Rodday"]["common_ROV_ASes_of_all_measurements_list"] = common_ROV_ASes
    ROV_ASes_dict_results["TMA_paper_2021_Rodday"]["common_ROV_ASes_of_all_measurements_count"] = len(common_ROV_ASes)


def find_common_union_ROV_ASes_of_all_datasets(ROV_ASes_dict_results):
    all_ROV_lists = [
        ROV_ASes_dict_results["TMA_paper_2021_Rodday"]["union_ROV_ASes_of_all_measurements_list"],
        ROV_ASes_dict_results["ROV_Deployment_monitor"]["ROV_ASes_list"],
        ROV_ASes_dict_results["IsBGPSafeYet_Cloudflare"]["ROV_ASes_list"]
    ]
    union_ROV_ASes = list(set([item for sublist in all_ROV_lists for item in sublist]))
    common_ROV_ASes = list(set(all_ROV_lists[0]).intersection(*all_ROV_lists))

    ROV_ASes_dict_results["union_ROV_ASes_of_all_datasets_list"] = union_ROV_ASes
    ROV_ASes_dict_results["union_ROV_ASes_of_all_datasets_count"] = len(union_ROV_ASes)
    ROV_ASes_dict_results["common_ROV_ASes_of_all_datasets_list"] = common_ROV_ASes
    ROV_ASes_dict_results["common_ROV_ASes_of_all_datasets_count"] = len(common_ROV_ASes)


if __name__ == '__main__':

    ROV_ASes_dict_results = NestedDict()
    find_common_union_ROV_ASes_Active_Measurements_TMA_paper_2021_Rodday_data(
        "../datasets/ROV-Active-Measurements-TMA-Paper/",
        ["20210703", "20210705", "20210709", "20210717", "20210719"],
        ROV_ASes_dict_results
    )
    ROV_ASes_dict_results["ROV_Deployment_monitor"]["ROV_ASes_list"] = load_ROV_Deployment_monitor_data(
        "../datasets/ROV-Deployment-Monitor/2020-08-31.csv"
    )
    ROV_ASes_dict_results["ROV_Deployment_monitor"]["ROV_ASes_count"] = len(
        ROV_ASes_dict_results["ROV_Deployment_monitor"]["ROV_ASes_list"]
    )
    ROV_ASes_dict_results["IsBGPSafeYet_Cloudflare"]["ROV_ASes_list"] = load_Is_BGP_Safe_Yet_Cloudflare_ASes(
        "../datasets/IsBGPSafeYet-Cloudflare/27-03-2022.csv"
    )
    ROV_ASes_dict_results["IsBGPSafeYet_Cloudflare"]["ROV_ASes_count"] = len(
        ROV_ASes_dict_results["IsBGPSafeYet_Cloudflare"]["ROV_ASes_list"]
    )

    find_common_union_ROV_ASes_of_all_datasets(ROV_ASes_dict_results)

    print(ROV_ASes_dict_results)
    write_results_to_json(ROV_ASes_dict_results, "./evaluation_data/forth_ypourgeio_project/ROV_ASes_results.json")