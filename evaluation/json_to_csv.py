import json
import csv

def read_json_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0

if __name__ == '__main__':
    json_data = read_json_data(r'as_country_vuln_ranking.json')

    with open('country_ranking.csv', 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Country", "Ranking_Score"])
        for key, value in json_data["country_vuln_ranking"].items():
            writer.writerow([key, value])