import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.use('Agg')
import matplotlib.pyplot as plt

pos_data = [2246,4175,7491,17089,3699] #positive
neg_data=[540388,1438226,2027958,1596290,269799] #Negative

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.2f}%\n({:d})".format(pct, absolute)

def draw_s1(data,title_name,save_file):
    fig, ax = plt.subplots(figsize=(10, 4), dpi=300, subplot_kw=dict(aspect="equal"))
    label = ["0","1","2","3","4"]
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="k"),colors=["#B2EBF2","#4DD0E1","#00BCD4","#0097A7","#006064"])

    ax.legend(wedges, label,
            title="Number of annotation categories",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title(title_name)
    plt.savefig("./"+save_file)

draw_s1(pos_data,"Positive","fig_s2a_pos.png")
draw_s1(neg_data,"Negative","fig_s2a_neg.png")

