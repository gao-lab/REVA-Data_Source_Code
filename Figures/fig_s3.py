import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def draw_bar():
    #conservation F1-score
    labels=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    temp=np.loadtxt(open("../Data/f1_clinvar.txt",'r'),delimiter="\t",dtype=np.float)

    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6),dpi=300)
    ax.grid(False)
    color_list=["#63b2ee","#76da91","#f8cb7f","#f89588","#7cd6cf","#9192ab"]

    rects1 = ax.bar(x - 2.5*width, temp[0], width, label='All',edgecolor='k',color=color_list[0])
    rects2 = ax.bar(x - 1.5*width, temp[1], width, label='All ClinVar',edgecolor='k',color=color_list[1])
    rects3 = ax.bar(x - 0.5*width, temp[2], width, label='Benign',edgecolor='k',color=color_list[2])
    rects4 = ax.bar(x + 0.5*width, temp[3], width, label='Likely benign',edgecolor='k',color=color_list[3])
    rects5 = ax.bar(x + 1.5*width, temp[4], width, label='Drug response',edgecolor='k',color=color_list[4])
    rects6 = ax.bar(x + 2.5*width, temp[5], width, label='Others',edgecolor='k',color=color_list[5])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1 score',fontsize=18)
    #ax.set_xlabel('Tool')
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.legend(frameon=False,fontsize=12)
    fig.tight_layout()
    plt.savefig("./fig_s3.png")

draw_bar()