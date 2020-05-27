import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pandas as pd

sns.set(style = "whitegrid")
data = pd.read_csv('../Data/bacc_f1_result.txt',sep='\t')
data_sort = data.sort_values(by=['F1score'])

x = data_sort.balanced_acc
z = data_sort.F1score

y = range(1,11,1)
cm = plt.cm.get_cmap('coolwarm')


fig,ax = plt.subplots(dpi=300)

bubble = ax.scatter(x, y, s = 200, c = z, cmap = cm, linewidth = 0.5, alpha = 1) #make bubble plot, the s is the size of bubble.
ax.grid()
cbar = fig.colorbar(bubble)
cbar.set_label('F1 Score',labelpad=-20, y=1.1,rotation=0,size=10) # set the label of the legend colorbar
cbar.ax.tick_params(labelsize=10)
ax.set_ylim(0,11) # To make the y axis label in the middle position
plt.yticks(y,data_sort.Tools) # Here we need use plt.yticks to match the y and label, if we use as.set_yticklabels, the label position will be wrong
ax.set_xlabel('Balanced Accuracy',fontsize=10)
ax.xaxis.set_tick_params(labelsize=10)
ax.yaxis.set_tick_params(labelsize=10)


ax.spines['top'].set_visible(False) # Do not have the spines of right
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')

ax.tick_params(top='off',bottom='on',left='on',right='off') # Do not have the scale of the right and top.

plt.tight_layout() #Make all information showed on the picture.
plt.savefig("./pics/fig_2a.png")