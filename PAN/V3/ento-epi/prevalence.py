# Plot pathogen prevalence for TP13 releases
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


palette = sns.color_palette("icefire")
sns.set(font='Arial', font_scale=0.80)
sns.set_palette(palette)
sns.set_style('ticks')

# read in human states data
df = pd.read_csv('H_Mean_0001.csv')
days = df.shape[0]
# df = pd.read_csv('/Users/agastyamondal/H_Mean_0001.csv')
# extract labels for prevalence states
labels = "^A|^U|^T|^D"
df = df.filter(regex=labels)

# calculate all-ages prevalence
age_idx = ["00_01", "01_02", "02_03", "03_04", "04_05", "05_06"]
age_idx = {
    '00_01': '0-5',
    '01_02': '5-17',
    '02_03': '17-40',
    '03_04': '40-60',
    '04_05': '60-99',
    '05_06': '99+'
}
prev_df = pd.DataFrame()
for idx in age_idx.keys():
    prev_df[age_idx[idx]] = df.filter(regex=idx).sum(axis=1)

prev_df['All-ages'] = prev_df.sum(axis=1)
prev_df['Time'] = df['Time']

rel_times = [730, 737, 744, 751, 758, 765, 772, 779]
prev_df_melt = prev_df.melt('Time', var_name='cols', value_name='vals')
prev_df_melt.rename(columns={'cols': 'Age Group (yrs)'}, inplace=True)

fig, ax = plt.subplots(figsize=(20,6))
g = sns.lineplot(
    x="Time", y="vals", hue='Age Group (yrs)', data=prev_df_melt, lw=2.5,
    palette=[
        '#0d3b66', 
        '#bbd0ff', '#b8c0ff', '#c8b6ff', 
        '#e7c6ff', '#ffd6ff', '#d8d8d8', 
    ][::-1],
    alpha=0.85
)
# g.set_title('Epidemiological Dynamics - Human Infection Prevalence')
# g.set(xlabel='Time (day)', ylabel='P. falciparum Prevalence')
for i in rel_times:
    x = ax.axvline(i, alpha=0.5, lw=1)
    x.set_zorder(5)
ax.set_aspect(0.15*days/(0.02+0.02*0.25))
ax.set_xlim(0, days)
ax.set_ylim(0, 0.02+0.02*0.25)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_title("")
ax.get_legend().remove()


# %%
g.figure.savefig(
    'prevalence.tiff', dpi=300,
    transparent=True, bbox_inches='tight', 
    pad_inches=0.1
)
# %%
