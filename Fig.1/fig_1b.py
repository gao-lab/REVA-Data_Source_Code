import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

pos_ratios=[0.1519,0.3550,0.4932]
neg_ratios=[0.0699,0.3944,0.5357]

def draw_pie(ratios,title_name,save_file):
    fig, ax = plt.subplots(figsize=(9, 6),dpi=300, subplot_kw=dict(aspect="equal"))
    labels = ['Others', 'Intron', 'Intergenic region']
    angle = -180 * ratios[0]
    ax.pie(ratios, autopct='%1.2f%%', startangle=angle,
        labels=labels,colors=["#00A087B2","#E64B35B2","#3C5488B2"])
    ax.set_title(title_name)
    plt.savefig("./pics/"+save_file)

draw_pie(pos_ratios,"Positive variants","fig_1b_pos.png")
draw_pie(neg_ratios,"Negative variants","fig_1b_neg.png")