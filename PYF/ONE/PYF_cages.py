

from os import path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


(PTH, FNM) = (
    '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/cages/',
    'pgSIT_Adults'
)
SHT = [
    'Generation_1', 'Generation_2', 'Generation_3', 
    'Generation_4', 'Generation_5', 'Generation_6', 
    'Key'
]
# COLS = (
#     ('#2614ed', 'v'), ('#ff006e', 'o'), ('#8338ec', '*'), ('#ffe83d', '+'),
#     ('#22a5f1', 'X'), ('#45d40c', '2'), ('#f00fbf', 'p'), ('#000000', 's')
# )
COLS = (
    ('#45d40c', 's', 1), 
    ('#ff006e', 'o', 1), ('#C703FC', 'v', 1), 
    ('#9a92f7', '*', 1), ('#7367f4', '+', 1), ('#5446F1', 'X', 1), 
    ('#4333F0', '2', 1), ('#2614ed', 'p', 1)
)
###############################################################################
# Load data
###############################################################################
dfDict = pd.read_excel(path.join(PTH, FNM+'.xls'), sheet_name=SHT)
###############################################################################
# Slicing and Plotting
###############################################################################
cols = [
    'Hatching rate', 'Hatched selected egg #', 
    'Left egg #', 'Hatched left egg #'
]

(fig, ax) = plt.subplots()
for i in range(8):
    series = []
    for page in SHT[:-1]:
        dfSlice = dfDict[page].iloc[(i*3):(i*3+3)]
        dataParts = zip(
            list(dfSlice[cols[0]]), list(dfSlice[cols[1]]),
            list(dfSlice[cols[2]]), list(dfSlice[cols[3]])
        )
        data = [(b+d)/(a+c) if (a+c) > 0 else 0 for (a, b, c, d) in dataParts]
        series.append(data)
    dSeries = np.asarray(series).T
    shp = dSeries.shape

    for j in dSeries:
        plt.plot(range(1, shp[1]+1), j, 
            alpha=.7, lw=1,
            color=COLS[i][0]# , marker=COLS[i][1]
        )
plt.vlines(
    range(1, 7), 0, 1, 
    alpha=.25, lw=.2, ls='--'
)
plt.hlines(
    np.arange(0, 1, .25), 1, 6, 
    alpha=.25, lw=.25, ls='--'
)
# ax.set_xticks([])
# ax.set_yticks([])
ax.set_axis_off()
ax.set_ylim(-.1, 1.1)
ax.set_aspect(5)
fig.savefig(
    path.join(PTH, FNM+'.png'), 
    dpi=750, pad_inches=0, bbox_inches='tight'
)