

from os import path
import numpy as np
import pandas as pd
import pylab
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
    ('#2b2c7c', None, .6, ':', .6, '50 WT♂:50 WT♀'), 
    ('#ff006e', None, .6, ':', .6, '50 gRNA-myo+β-Tub/gRNA-myo+β-Tub♂:50 gRNA-myo+β-Tub/gRNA-myo+β-Tub ♀'),  
    ('#45d40c', None, .6, ':', .6, '50 Nup-50 cas9/Nup-50 cas9♂:50 WT♀'), 
    ('#268CFF', None, .6, '-', .7, '50 pgSIT♂ :50 WT♂:50 WT♀'),  
    ('#6f2082', 'o', .65, '-', .75, '250 pgSIT♂ :50 WT♂:50 WT♀'), 
    ('#ff006e', None, .7, '-', .8, '500 pgSIT♂ :50 WT♂:50 WT♀'),  
    ('#009aa3', 'o', .75, '-', .85, '1000 pgSIT♂ :50 WT♂:50 WT♀'),  
    ('#2614ed', None, .8, '-', .9, '2000 pgSIT♂ :50 WT♂:50 WT♀')
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

        for (ix, j) in enumerate(dSeries):
            if (ix % 3 == 0):
                ax.plot(range(1, shp[1]+1), j, 
                    alpha=.85*COLS[i][4], 
                    lw=2*COLS[i][2],
                    color=COLS[i][0],
                    marker=COLS[i][1],
                    markersize=2.5,
                    ls=COLS[i][3],
                    label=COLS[i][-1]
                )
            else:
                ax.plot(range(1, shp[1]+1), j, 
                    alpha=.85*COLS[i][4], 
                    lw=2*COLS[i][2],
                    color=COLS[i][0],
                    marker=COLS[i][1],
                    markersize=2.5,
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
        path.join(PTH, fnm+'.pdf'), 
        dpi=750, pad_inches=.05, bbox_inches='tight'
    )




###############################################################################
# Legend Hack
###############################################################################
dfDict = pd.read_excel(path.join(PTH, fnm+'.xls'), sheet_name=SHT)
(fig, ax) = plt.subplots()
figlegend = pylab.figure(figsize=(3,2))
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

    for (ix, j) in enumerate(dSeries):
        if (ix % 3 == 0):
            ax.plot(range(1, shp[1]+1), j, 
                alpha=1*COLS[i][4], 
                lw=2.5,
                color=COLS[i][0],
                marker=COLS[i][1],
                markersize=5,
                ls=COLS[i][3],
                label=COLS[i][-1]
            )
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
figLegend = pylab.figure(figsize = (6.475, 1.8))
# produce a legend for the objects in the other figure
pylab.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left')
# create a second figure for the legend
figLegend.savefig(path.join(PTH, 'legend.pdf'))
