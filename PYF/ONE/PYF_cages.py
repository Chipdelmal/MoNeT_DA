

from os import path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


(PTH, FNM) = (
    '/home/chipdelmal/Documents/WorkSims/PYF/Onetahi/cages/', 
    ('pgSIT_Adults', 'pgSIT_Eggs')
)
SHT = [
    'Generation_1', 'Generation_2', 'Generation_3', 
    'Generation_4', 'Generation_5', 'Generation_6', 
    'Key'
]
COLS = (
    ('#f00fbf', 's', .6, ':', .6), 
    ('#ff006e', 'o', .6, ':', .6),  ('#45d40c', 'v', .6, ':', .6), 
    ('#268CFF', '*', .6, '-', .7),  ('#6f2082', '+', .65, '-', .75), 
    ('#ff006e', 'X', .7, '-', .8),  ('#009aa3', '2', .75, '-', .85),  
    ('#2614ed', 'p', .8, '-', .9)
)
###############################################################################
# Load data
###############################################################################
for fnm in FNM:
    dfDict = pd.read_excel(path.join(PTH, fnm+'.xls'), sheet_name=SHT)
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
                alpha=.85*COLS[i][-1], 
                lw=1.2*COLS[i][2],
                color=COLS[i][0],
                # marker=COLS[i][1],
                ls=COLS[i][3]
            )
    plt.vlines(
        range(1, 7), 0, 1, 
        alpha=.2, lw=.2, ls=':'
    )
    plt.hlines(
        np.arange(0, 1, .25), 1, 6, 
        alpha=.2, lw=.2, ls=':'
    )
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.set_axis_off()
    ax.set_xlim(1, 6)
    ax.set_ylim(0, 1)
    ax.set_aspect(5)
    fig.tight_layout()
    fig.savefig(
        path.join(PTH, fnm+'.png'), 
        dpi=750, pad_inches=.05, bbox_inches='tight'
    )