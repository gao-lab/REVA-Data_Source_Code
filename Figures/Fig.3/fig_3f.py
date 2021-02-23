import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def draw_bar():
    #conservation F1-score
    labels=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    temp=np.loadtxt(open("../../Data/f1_hgmd.txt",'r'),delimiter="\t",dtype=np.float)

    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots(figsize=(8, 8),dpi=300)
    ax.grid(False)
    color_list=["#63b2ee","#76da91","#f8cb7f","#f89588","#7cd6cf","#9192ab"]

    rects1 = ax.bar(x - 2.5*width, temp[0], width, label='All',edgecolor='k',color=color_list[0])
    rects2 = ax.bar(x - 1.5*width, temp[1], width, label='All HGMD',edgecolor='k',color=color_list[1])
    rects3 = ax.bar(x - 0.5*width, temp[2], width, label='DM?',edgecolor='k',color=color_list[2])
    rects4 = ax.bar(x + 0.5*width, temp[3], width, label='DP',edgecolor='k',color=color_list[3])
    rects5 = ax.bar(x + 1.5*width, temp[4], width, label='FP',edgecolor='k',color=color_list[4])
    rects6 = ax.bar(x + 2.5*width, temp[5], width, label='DFP',edgecolor='k',color=color_list[5])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1 score',fontsize=20)
    #ax.set_xlabel('Tool')
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.legend(frameon=False,fontsize=12)
    fig.tight_layout()
    plt.savefig("./fig_3f.png")

draw_bar()