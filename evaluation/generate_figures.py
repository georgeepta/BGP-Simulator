import matplotlib.pyplot as plt


if __name__ == '__main__':
    x1 = list(range(0, 101, 10))
    y1 = [0.4808897687266289,
          0.33521264428966013,
          0.53102309618966,
          0.430252186030732,
          0.5021746038229549,
          0.4542759741227817,
          0.3912974915420401,
          0.4563000503983046,
          0.485922051037982,
          0.47532848155483887,
          0.4378020564157861
          ]
    plt.plot(x1, y1, marker='o', label="ROV adoption prob. 0.25")
    plt.xticks(x1, list(range(0, 101, 10)))
    plt.yticks([v * 0.1 for v in range(0, 11, 1)])
    plt.xlabel('Expected ROV Deployment (top ISPs)')
    # Set the y axis label of the current axis.
    plt.ylabel('Attacker’s Success Rate')
    # Set a title of the current axes.
    plt.title('Prefix hijack success rate')
    # show a legend on the plot
    plt.legend()
    #save figure
    plt.savefig('./figures/1_prefix_hijack_rov_only_top.png')
    # Display a figure.
    plt.show()