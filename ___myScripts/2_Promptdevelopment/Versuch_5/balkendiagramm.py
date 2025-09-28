import matplotlib.pyplot as plt
import numpy as np
import os

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

def createBarChart(evaluationllms:tuple, extractionmodelresults:dict):

    x = np.arange(len(evaluationllms))*1.3  # the label locations
    width = 0.18  # the width of the bars
    multiplier = -1

    # hatches = ['/', '\\', 'x', 'o', '.', 'O', '*']

    fig, ax = plt.subplots(layout='constrained', figsize=(10, 6))
    gap = 0.02
    for i, (attribute, measurement) in enumerate(extractionmodelresults.items()):
        offset = multiplier * (width + gap)  # 👈 add gap
        rects = ax.bar(
            x + offset, 
            measurement, 
            width, 
            label=attribute, 
            # hatch=hatches[i % len(hatches)],   # add structure
            alpha=1                          # slight transparency
        )
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Evaluationmodel')
    ax.set_ylabel('Ø Hitrate [%]')
    ax.set_title('LLM performance comparison')
    ax.set_xticks(x + width, evaluationllms)
    ax.legend(loc='upper right', ncols=1, title="Generationmodel")
    ax.set_ylim(0, 140)

    savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "balken", "test.png"]
    savepath = os.path.join(*savepathparts)
    fig.savefig(savepath, bbox_inches='tight', dpi=300)

evaluationllms = ("Llama3.2:1.5b", "Llama3.2:3b", "Llama3:8b", "Llama3.3:70b", "Llama3.2:20b")
extractionmodelresults = {
    'deepseek-r1:1.5b': (83, 43, 98, 22, 22),
    'deepseek-r1:8b': (79, 83, 50, 19, 44),
    'deepseek-r1_32b': (85, 32, 11, 44, 55),
    'deepseek-r1_70b': (95, 82, 19, 50, 66),
    'deepseek-r1_20b': (95, 82, 19, 50, 66),
}
# createBarChart(evaluationllms, extractionmodelresults)