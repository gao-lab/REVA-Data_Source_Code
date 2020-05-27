import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def draw_bar():
    #annotation number
    labels = ['DNA Accessibility', 'Transcription Factor', 'Histone Modification', 'DNA Methylation']
    pos_data = [0.994359456,23.4950574,5.473492294,0.209811127]
    neg_data = [0.662586162,2.840739999,3.638789349,0.171628792]

    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots(figsize=(8, 6),dpi=300)

    rects1 = ax.bar(x - width/2, pos_data, width, label='Positive',color='orange',edgecolor='k')
    rects2 = ax.bar(x + width/2, neg_data, width, label='Negative',color='royalblue',edgecolor='k')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average Number of Annotations')
    ax.set_xlabel('Feature Category')
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.savefig("./pics/fig_s1b.png")

draw_bar()