import matplotlib.pyplot as plt
import numpy as np
import os

def multipieplot(context_data_list:list, bfr_data_list:list, title_list:list, name:str):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    outercolors = ["#56B4E9", "#E69F00", "#0072B2", "#CC79A7", "#F0E442", "#009E73"]
    innercolors = ["#B1B1B1", "#636363"]
    size = 0.3
    for ax, bfr_data, context_data, title in zip(axs.flat, bfr_data_list, context_data_list, title_list):
        # General numbers
        bfr_sum = sum(bfr_data)

        # Outer ring
        outer_wedges, _ = ax.pie(
            bfr_data,
            radius=1,
            wedgeprops=dict(width=size, edgecolor='w'),
            colors=outercolors,
            startangle=90
        )
        outer_labels = []
        for sizeparameter in bfr_data:
            if sizeparameter > 0:
                outer_labels.append(f"{round(sizeparameter/bfr_sum*100, 1)}%")
            else:
                outer_labels.append("")
        # 
        for k, wedge in enumerate(outer_wedges):
            ang = (wedge.theta2 + wedge.theta1) / 2
            x = np.cos(np.deg2rad(ang))
            y = np.sin(np.deg2rad(ang))

            x_start, y_start = x * (1 * 0.5), y * (1* 0.5)
            x_end_text, y_end_text = x * .85, y * .85

            # ax.plot([x_start, x_end_line], [y_start, y_end_line], color='black', lw=0.8)
            ax.text(x_end_text, y_end_text, outer_labels[k], ha='center', va='center')

        # Inner ring
        inner_wedges, _ = ax.pie(
            context_data,
            radius = 1-size,
            wedgeprops = dict(width=size, edgecolor='w'),
            colors=innercolors,
            startangle=90
        )
        inner_labels = [f"{round(context_data[0]/(context_data[0]+context_data[1])*100, 1)}%", f"{round(context_data[1]/(context_data[0]+context_data[1])*100, 1)}%"]
        for j, wedge in enumerate(inner_wedges):
            ang = (wedge.theta2 + wedge.theta1) / 2 # angle of wedge
            x = np.cos(np.deg2rad(ang)) # x coord of center
            y = np.sin(np.deg2rad(ang)) # y coord of center

            # Starting point (on wedge), and label location
            # x_start, y_start = x * (1 * 0.5), y * (1 * 0.5)
            # x_end_line, y_end_line = x * 1.3, y * 1.3
            x_end_text, y_end_text = x * .55, y * .55

            ax.text(x_end_text, y_end_text, inner_labels[j], ha='center', va='center')

        ax.set_title(title[1], y=0.87, fontsize=16)
        ax.axis('equal')
        ax.text(1.05, -1, "Context", ha='left', va='center')
        ax.plot([-.5, -1], [0.7, 1], color='black', lw=0.8)
        ax.text(-1.05, 1, "Basefailurerate", ha='right', va='center')
        ax.plot([.3, 1], [-0.45, -1], color='black', lw=0.8)
        ax.text(
            0.5, 0.1, title[0], 
            transform=ax.transAxes,
            ha="center", va="top",
            fontsize=10, color="gray"
        )

    fig.legend(['True Positive', 'False Negative', 'False Null', 'False Positive', 'True Negative', 'True Null', 'Good Context', 'Bad Context'], loc="upper right", title="Categories", bbox_to_anchor=(0.97, 0.97))
    plt.tight_layout(rect=[0, 0, 0.85, 1], pad=2)
    plt.show()

    savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "checkresultsplots", name, ".png"]
    savepath = os.path.join(*savepathparts)
    # plt.savefig(savepath)

# ---- TESTING ----
# Example data for pies
data_a = [
    [30, 20, 50, 30, 20, 10],
    [10, 40, 50, 10, 20, 30],
    [25, 25, 25, 25, 10, 15],
    [15, 30, 25, 0, 10, 5]
]

data_b = [
    [10, 50],
    [12, 48],
    [10, 30],
    [20, 30]
]

titles = [
    ['„How high is the base failure rate (BFR) of [itemname]?“', 'Prompt 1'],
    ['„How high is the base failure rate (BFR) of [itemname]?“', 'Prompt 2'],
    ['„How high is the base failure rate (BFR) of [itemname]?“', 'Prompt 3'],
    ['„How high is the base failure rate (BFR) of [itemname]?“', 'Prompt 4']
]

multipieplot(data_b, data_a, titles, "test")