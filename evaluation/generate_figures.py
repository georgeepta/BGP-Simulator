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


def plot_today_rov_status_vs_top_isps_other_random_prop_prefix_hijacking(evaluation_results):
    x1 = [v * 0.1 for v in range(0, 11, 1)]
    y1 = []
    for item in evaluation_results["today_rov_status_other_random_prop"]["prefix_hijacking"]:
        y1.append(evaluation_results["today_rov_status_other_random_prop"]["prefix_hijacking"][item])

    y2 = []
    for item in evaluation_results["top_isps_rov_other_random_prop"]["prefix_hijacking"]:
        y2.append(evaluation_results["top_isps_rov_other_random_prop"]["prefix_hijacking"][item])

    plt.figure(3)
    plt.plot(x1, y1, linestyle='dashed', marker='s', color='tab:red', label="Today's ROV status")
    plt.plot(x1, y2, linestyle='solid', marker='+', color='tab:green', label="Top 100 ISPs perform ROV")
    plt.xticks([v * 0.1 for v in range(0, 11, 1)])
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.xlabel('Deployment Probability of other ASes')
    # Set the y axis label of the current axis.
    plt.ylabel('Attacker’s Success Rate')
    # Set a title of the current axes.
    plt.title('Prefix hijack success rate')
    # show a legend on the plot
    plt.legend()
    # save figure
    plt.savefig('./figures/today_rov_status_vs_top_isps_other_random_prop_prefix_hijacking.png')


def plot_today_rov_status_vs_top_isps_other_random_prop_subprefix_hijacking(evaluation_results):
    x1 = [v * 0.1 for v in range(0, 11, 1)]
    y1 = []
    for item in evaluation_results["today_rov_status_other_random_prop"]["subprefix_hijacking"]:
        y1.append(evaluation_results["today_rov_status_other_random_prop"]["subprefix_hijacking"][item])

    y2 = []
    for item in evaluation_results["top_isps_rov_other_random_prop"]["subprefix_hijacking"]:
        y2.append(evaluation_results["top_isps_rov_other_random_prop"]["subprefix_hijacking"][item])

    plt.figure(4)
    plt.plot(x1, y1, linestyle='dashed', marker='s', color='tab:red', label="Today's ROV status")
    plt.plot(x1, y2, linestyle='solid', marker='+', color='tab:green', label="Top 100 ISPs perform ROV")
    plt.xticks([v * 0.1 for v in range(0, 11, 1)])
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.xlabel('Deployment Probability of other ASes')
    # Set the y axis label of the current axis.
    plt.ylabel('Attacker’s Success Rate')
    # Set a title of the current axes.
    plt.title('Subprefix hijack success rate')
    # show a legend on the plot
    plt.legend()
    # save figure
    plt.savefig('./figures/today_rov_status_vs_top_isps_other_random_prop_subprefix_hijacking.png')


def plot_simulator_average_accuracy_prefix_hijacks(accuracy_results):
    x1 = list(accuracy_results["prefix_hijacks"].keys())
    avg_accuracy_id = x1.pop()
    y1 = list(accuracy_results["prefix_hijacks"].values())
    avg_accuracy_value = y1.pop()

    plt.figure(5)
    plt.bar(x1, y1, linestyle='solid', width=0.5, color='peru', label="Accuracy per hijack")
    plt.xticks(x1, rotation=50, fontsize=5, ha='right')
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.axhline(y=avg_accuracy_value, linestyle='dashed', linewidth=2, color='tab:green', label='Mean Accuracy')

    plt.xlabel('Historical Hijack ID')
    # Set the y axis label of the current axis.
    plt.ylabel('Accuracy')
    # Set a title of the current axes.
    plt.title('Simulator Accuracy to detect the infected ASes (Prefix Hijacks)')
    # show a legend on the plot
    plt.legend()
    # save figure
    plt.savefig('./figures/simulator_accuracy_prefix_hijacks.png', dpi=300, bbox_inches="tight")


def plot_simulator_average_accuracy_subprefix_hijacks(accuracy_results):
    x1 = list(accuracy_results["subprefix_hijacks"].keys())
    avg_accuracy_id = x1.pop()
    y1 = list(accuracy_results["subprefix_hijacks"].values())
    avg_accuracy_value = y1.pop()

    plt.figure(6)
    plt.bar(x1, y1, linestyle='solid', width=0.3, color='coral', label="Accuracy per hijack")
    plt.xticks(x1, rotation=50, fontsize=5, ha='right')
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])

    plt.axhline(y=avg_accuracy_value, linestyle='dashed', linewidth=2, color='tab:green', label='Mean Accuracy')

    plt.xlabel('Historical Hijack ID')
    # Set the y axis label of the current axis.
    plt.ylabel('Accuracy')
    # Set a title of the current axes.
    plt.title('Simulator Accuracy to detect the infected ASes (Subprefix Hijacks)')
    # show a legend on the plot
    plt.legend(loc='lower right')
    # save figure
    plt.savefig('./figures/simulator_accuracy_subprefix_hijacks.png', dpi=300, bbox_inches="tight")


if __name__ == '__main__':

    evaluation_results = read_evaluation_results("evaluation_results.json")
    rpki_adoption_propability_list = [0.25, 0.50, 0.75, 1.0]
    for prop in rpki_adoption_propability_list:
        plot_prop_line_collateral_benefit_prefix_hijacking(prop, evaluation_results)

    for prop in rpki_adoption_propability_list:
        plot_prop_line_collateral_benefit_subprefix_hijacking(prop, evaluation_results)

    plot_today_rov_status_vs_top_isps_other_random_prop_prefix_hijacking(evaluation_results)
    plot_today_rov_status_vs_top_isps_other_random_prop_subprefix_hijacking(evaluation_results)

    accuracy_results = read_evaluation_results("accuracy_results.json")
    plot_simulator_average_accuracy_prefix_hijacks(accuracy_results)
    plot_simulator_average_accuracy_subprefix_hijacks(accuracy_results)

    # Display a figure.
    #plt.show()