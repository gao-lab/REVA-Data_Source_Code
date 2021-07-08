import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

pos_ratios=[0.1408,0.3596,0.4996]
neg_ratios=[0.0655,0.3962,0.5383]

def draw_pie(ratios,title_name,save_file):
    fig, ax = plt.subplots(figsize=(9, 6),dpi=300, subplot_kw=dict(aspect="equal"))
    labels = ['Others', 'Intron', 'Intergenic region']
    angle = -180 * ratios[0]
    matplotlib.rcParams['font.size'] = 15
    patches, texts, autotexts=ax.pie(ratios, autopct='%1.2f%%', startangle=angle,
        labels=labels,colors=["#00A087B2","#E64B35B2","#3C5488B2"])
    [_.set_fontsize(15) for _ in texts]
    ax.set_title(title_name,fontsize=16)
    plt.savefig(save_file)
    

draw_pie(pos_ratios,"Positive variants","./fig_2a_pos.png")
draw_pie(neg_ratios,"Negative variants","./fig_2a_neg.png")
