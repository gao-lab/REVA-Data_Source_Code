import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts



cell_list=["All","GM18507","HEK293T","HepG2","K562","K562_GATA1","NA12878&NA19239","SH-SY5H"]
tool_list=["CADD","DeepSEA","Eigen","Eigen-PC","ExPecto","FunSeq2","GWAVA-Region","GWAVA-TSS","GWAVA-Unmatch"]
f1_score=np.array([[0.0156,0.0559,0.0160,0.0318,0.0094,0.0183,0.0273,0.0233,0.0366],
                  [0.0801,0.0836,0.1178,0.1381,0.0121,0.0293,0.0727,0.1005,0.1467],
                  [0.1109,0.0556,0.2039,0.2669,0.0037,0.0125,0.0552,0.1358,0.2009],
                  [0.0052,0.0270,0.0050,0.0108,0.0067,0.0092,0.0098,0.0085,0.0088],
                  [0.0097,0.0418,0.0092,0.0184,0.0093,0.0181,0.0185,0.0127,0.0236],
                  [0.0444,0.1194,0.0594,0.0707,np.nan,np.nan,0.0984,0.0465,0.0853],
                  [0.1779,0.2375,0.2973,0.3746,0.0811,0.0469,0.1599,0.1338,0.3285],
                  [0.1176,np.nan,0.1101,0.0870,np.nan,np.nan,np.nan,0.0465,0.0417]])

fig, ax = plt.subplots(dpi=300)
#im, cbar = heatmap(f1_score, cell_list, tool_list, ax=ax,
#                   cmap="YlGn", cbarlabel="F1 Score")
#im, cbar = heatmap(balanced_acc, cell_list, tool_list, ax=ax,
#                   cmap="YlOrBr", cbarlabel="Balanced Accuracy")
im, cbar = heatmap(auc_score, cell_list, tool_list, ax=ax,
                   cmap="YlOrRd", cbarlabel="AUC")
def func(x, pos):
    return "{:.3f}".format(x).replace("0.", ".").replace(".000", "N.A")
texts = annotate_heatmap(im, valfmt=matplotlib.ticker.FuncFormatter(func),size=9)
fig.tight_layout()
plt.savefig("./pics/fig_2e.png")