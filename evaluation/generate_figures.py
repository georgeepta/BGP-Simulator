import json
import matplotlib.pyplot as plt


def read_evaluation_results(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Sorry, the file, "+ file_path + " ,does not exist.")
        return 0


def plot_prop_line_collateral_benefit_prefix_hijacking(prop_value, evaluation_results):
    x1 = list(range(0, 101, 10))
    y1 = []
    for item in evaluation_results["collateral_benefit"]["prefix_hijacking"]:
        y1.append(evaluation_results["collateral_benefit"]["prefix_hijacking"][item][str(prop_value)])
    label_str = "ROV adoption prob. "+str(prop_value)

    plt.figure(1)
    if prop_value == 0.25:
        plt.plot(x1, y1, marker='s', color='tab:green', label=label_str)
    elif prop_value == 0.5:
        plt.plot(x1, y1, marker='o', color='tab:blue', label=label_str)
    elif prop_value == 0.75:
        plt.plot(x1, y1, marker='X', color='tab:orange', label=label_str)
    else:
        plt.plot(x1, y1, marker='D', color='tab:red', label=label_str)

    plt.xticks(x1, list(range(0, 101, 10)))
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.xlabel('Expected ROV Deployment (top ISPs)')
    # Set the y axis label of the current axis.
    plt.ylabel('Attacker’s Success Rate')
    # Set a title of the current axes.
    plt.title('Prefix hijack success rate')
    # show a legend on the plot
    plt.legend()
    # save figure
    plt.savefig('./figures/collateral_benefit_prefix_hijacking.png')


def plot_prop_line_collateral_benefit_subprefix_hijacking(prop_value, evaluation_results):
    x1 = list(range(0, 101, 10))
    y1 = []
    for item in evaluation_results["collateral_benefit"]["subprefix_hijacking"]:
        y1.append(evaluation_results["collateral_benefit"]["subprefix_hijacking"][item][str(prop_value)])
    label_str = "ROV adoption prob. "+str(prop_value)

    plt.figure(2)
    if prop_value == 0.25:
        plt.plot(x1, y1, marker='s', color='tab:green', label=label_str)
    elif prop_value == 0.5:
        plt.plot(x1, y1, marker='o', color='tab:blue', label=label_str)
    elif prop_value == 0.75:
        plt.plot(x1, y1, marker='X', color='tab:orange', label=label_str)
    else:
        plt.plot(x1, y1, marker='D', color='tab:red', label=label_str)

    plt.xticks(x1, list(range(0, 101, 10)))
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.xlabel('Expected ROV Deployment (top ISPs)')
    # Set the y axis label of the current axis.
    plt.ylabel('Attacker’s Success Rate')
    # Set a title of the current axes.
    plt.title('Subprefix hijack success rate')
    # show a legend on the plot
    plt.legend()
    # save figure
    plt.savefig('./figures/collateral_benefit_subprefix_hijacking.png')



if __name__ == '__main__':

    evaluation_results = read_evaluation_results("evaluation_results.json")
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1.0]
    for prop in rpki_adoption_propability_list:
        plot_prop_line_collateral_benefit_prefix_hijacking(prop, evaluation_results)

    for prop in rpki_adoption_propability_list:
        plot_prop_line_collateral_benefit_subprefix_hijacking(prop, evaluation_results)

    # Display a figure.
    plt.show()