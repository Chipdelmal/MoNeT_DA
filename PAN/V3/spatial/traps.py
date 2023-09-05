import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

palette = sns.light_palette('seagreen', reverse=True)
sns.set(font='Arial', font_scale=0.80)
sns.set_palette(palette)
sns.set_style('ticks')

base_dir = '/Users/sanchez.hmsc/Documents/GitHub/MoNeT_DA/PAN/V3/spatial/E_15_00500_00450000000_000100000000_0017500_0011700_0000000_0098700_0098700'
coords_df = pd.read_csv("STPD-max_25-10_CRD.csv", index_col=0)
coords_df = coords_df[(coords_df.lat < 0.17) & (coords_df.lon > 6.45) & (coords_df.lat > 0)]
coords_df =  coords_df.reset_index()
trap_idx =  [33, 34, 35, 36, 37]
files = os.listdir(base_dir)
# extract female mosquito files
fem_files = ['F_Mean_00' + str(i) + '.csv' for i in trap_idx]
for idx, _ in enumerate(fem_files):
    df = pd.read_csv(os.path.join(base_dir, fem_files[idx]))
    time = df['Time']
    df = df.drop('Time', axis=1)
    days = df.shape[0]-365

    # df['H'] = df['HH'] + df['HH'] + df['HR'] + df['HW']
    # df['R'] = df['HR'] + df['RR'] + df['RR'] + df['WR']
    # df['W'] = df['WW'] + df['HW'] + df['WR'] + df['WW']
    
    df['HH/HR'] = df['HH'] + df['HR']
    df['HW'] = df['HW']
    df['WW/WR'] = df['WW'] + df['WR']
    df['RR'] = df['RR']

    # lbsNot = ('HH', 'HR', 'HW', 'RR', 'WR', 'WW')
    lbsNot = ('HH', 'HR', 'WR', 'WW')
    [df.drop(i, axis=1, inplace=True) for i in lbsNot]

    # simulate weekly trap emptying
    emptying_times = time[time % 7 == 0]
    emptying_times = emptying_times[emptying_times != 0]
    trap_rows = []
    for t in emptying_times:
        row = df.iloc[[t]].values[0]
        trap_rows.append(pd.DataFrame(df.iloc[[t]]))
        rows_to_subtract = df.index[time >= t].tolist()
        df = df.apply(
            lambda x: x - row if x.name in rows_to_subtract else x, axis=1)
    trap_df = pd.concat(trap_rows)
    # trap_df = trap_df.div(trap_df.sum(axis=1), axis=0)
    trap_df['Time'] = time

    df_freq_melt = trap_df.melt('Time', var_name='cols', value_name='vals')
    df_freq_melt.rename(columns={'cols': 'Genotype'}, inplace=True)
    (fig, ax) = plt.subplots(figsize=(20,6))
    g = sns.lineplot(
        ax=ax,
        x="Time", y="vals", hue="Genotype", data=df_freq_melt,
        lw=5, alpha=0.95,
        palette=['#b388eb66', '#caffbf99', '#ff477e66', '#03045e66']
    )
    g.set(xlabel='Time (day)', ylabel='Genotype Frequency')
    yRan = 7.5e3
    ax.set_aspect(days/yRan)
    ax.set_xlim(15, days)
    ax.set_ylim(0, yRan)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.get_legend().remove()
    [x.set_linewidth(5) for x in ax.spines.values()]
    [x.set_edgecolor("#274c77BB") for x in ax.spines.values()]
    first_detection = trap_df[trap_df['HH/HR'] > 0].iloc[0].Time
    x = g.axvline(first_detection, color="#274c77BB", linewidth=2, zorder=-5)
    x.set_zorder(0)
    # Deal with 0-indexing in python compared to R...
    print(
        trap_idx[idx]-1, 
        str(int(coords_df.iloc[trap_idx[idx]-1].lat * 1e6)),
        str(int(coords_df.iloc[trap_idx[idx]-1].lon * 1e6))
    )
    lat_formatted = str(int(coords_df.iloc[trap_idx[idx]-1].lat * 1e6))
    lon_formatted = str(int(coords_df.iloc[trap_idx[idx]-1].lon * 1e6))
    filename = 'trap_freq_' + lat_formatted + '_' + lon_formatted + '.tiff'
    plt.savefig(
        filename, dpi=300,
        transparent=True, bbox_inches='tight', 
        pad_inches=0.1
    )
    plt.clf()

# (fig, ax) = plt.subplots(figsize=(20,6))
# ax.scatter(coords_df['lon'], coords_df['lat'])
# for idx in (32, 33, 34, 35, 36):
#     ax.text(
#         coords_df.iloc[idx].lon, coords_df.iloc[idx].lat, idx
        
#     )