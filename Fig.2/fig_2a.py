import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

# make figure and assign axis objects
fig = plt.figure(figsize=(12, 8),dpi=300)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
fig.subplots_adjust(wspace=0)
fig.suptitle('Negative', fontsize=12)
# pie chart parameters
#ratios = [.1708,.3596, .4996] #positive
ratios =[.0655, .3962, .5383] #negative
labels = ['Others', 'Intron', 'Intergenic region']
explode = [0.1, 0, 0]
# rotate so that first wedge is split by the x-axis
angle = -180 * ratios[0]
ax1.pie(ratios, autopct='%1.2f%%', startangle=angle,
        labels=labels, explode=explode,colors=["#91D1C2B2","#DC0000B2","#7E6148B2"])

# bar chart parameters

xpos = 0
bottom = 0
#ratios = [.0023, .0076, .0018, .1290] #positive
ratios = [.0005, .0060, .0003, .0587] #negative
width = .2
colors = ["#E64B35B2","#4DBBD5B2","#3C5488B2","#8491B4B2"]
bar_label=['Promoter','3\' UTR','5\' UTR', 'Mixed region']

for j in range(len(ratios)):
    height = ratios[-1-j]
    ax2.bar(xpos, height, width, bottom=bottom, color=colors[j],label=bar_label[j])
    ypos = bottom + ax2.patches[j].get_height() / 2
    bottom += height
    ax2.text(xpos, ypos, "%1.2f%%" % (ax2.patches[j].get_height() * 100),
             ha='center')
#ax2.set_title('Age of approvers')
h, l = ax2.get_legend_handles_labels()
ax2.legend(h[::-1], l)
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
# get the wedge data
theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
center, r = ax1.patches[0].center, ax1.patches[0].r
bar_height = sum([item.get_height() for item in ax2.patches])

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
                      coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
                      coordsB="data", axesA=ax2, axesB=ax1)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.savefig("./pics/fig_2a_neg.png")