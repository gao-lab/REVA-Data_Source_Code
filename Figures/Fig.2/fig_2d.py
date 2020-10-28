import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def draw_bar():
    #conservation F1-score
    labels=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    temp=np.loadtxt(open("../Data/f1_conv.txt",'r'),delimiter="\t",dtype=np.float)

    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6),dpi=300)
    color_list=["#B3E5FC","#4FC3F7","#03A9F4","#0288D1","#01579B"]

    rects1 = ax.bar(x - 2*width, temp[0], width, label='Conservation: 0-0.2',edgecolor='k',color=color_list[0])
    rects2 = ax.bar(x - width, temp[1], width, label='Conservation: 0.2-0.4',edgecolor='k',color=color_list[1])
    rects3 = ax.bar(x, temp[2], width, label='Conservation: 0.4-0.6',edgecolor='k',color=color_list[2])
    rects4 = ax.bar(x + width, temp[3], width, label='Conservation: 0.6-0.8',edgecolor='k',color=color_list[3])
    rects5 = ax.bar(x + 2*width, temp[4], width, label='Conservation: 0.8-1.0',edgecolor='k',color=color_list[4])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1 score')
    ax.set_xlabel('Tool')
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.savefig("./pics/fig_2d.png")

draw_bar()