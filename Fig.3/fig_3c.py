import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def draw_bar():
    #Gwas F1-score
    labels=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
    pos_data =[0.0446,0.0879,0.0361,0.0591,0.0115,0.0505,0.0572,0.0518,0.0645]
    neg_data =[0.0151,0.0552,0.0157,0.0313,0.0094,0.0175,0.0268,0.0226,0.0360]

    x = np.arange(len(labels))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots(figsize=(11, 6),dpi=300)

    rects1 = ax.bar(x - width/2, pos_data, width, label='Included in GWAS catalog',color='orange',edgecolor='k')
    rects2 = ax.bar(x + width/2, neg_data, width, label='Not Included in GWAS catalog',color='royalblue',edgecolor='k')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('F1 score')
    ax.set_xlabel('Tool')
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.savefig("./pics/fig_3c.png")

draw_bar()