# Plot clinical incidence (cases) for TP13 releases
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
days = df.shape[0]-2*365

age_idx = {
    '00_01': '0-5',
    '01_02': '5-17',
    '02_03': '17-40',
    '03_04': '40-60',
    '04_05': '60-99',
    '05_06': '99+'
}

# scale to be proportional to amount in each age group
age_proportions = {}
for idx in age_idx.keys():
    df_age = df.filter(regex=idx)
    # Get disease states
    df_age = df_age.filter(regex="^S|^T|^D|^A|^U|^P").sum(axis=1)
    age_proportions[idx] = df_age.iloc[0]

# extract labels for prevalence states
labels = "^clin_inc"
time = df['Time']
df = df.filter(regex=labels)

scaler = 100000
clininc_df = pd.DataFrame()
for idx in age_idx.keys():
    clininc_df[age_idx[idx]] = df.filter(
        regex=idx).sum(axis=1) * (scaler/age_proportions[idx])

clininc_df['All-ages'] = df.filter(regex=labels).sum(axis=1) * (scaler)
clininc_df['Time'] = time

# Remove weird dynamics at t=0
clininc_df.iloc[0] = None

clininc_df['60+'] = (clininc_df['60-99']+clininc_df['99+']) *(1/2)
clininc_df.drop('60-99', axis=1, inplace=True)
clininc_df.drop('99+', axis=1, inplace=True)

# scale by population/1000

clininc_df_melt = clininc_df.melt('Time', var_name='cols', value_name='vals')
clininc_df_melt.rename(columns={'cols': 'Age Group (yrs)'}, inplace=True)

fig, ax = plt.subplots(figsize=(20,6))
g = sns.lineplot(
    x="Time", y="vals", hue='Age Group (yrs)', data=clininc_df_melt, lw=2,
    palette=[
        '#d8d8d8', '#FDC4DC', '#c8b6ff', '#caffbf', 
        '#0d3b66', '#bbd0ff', 
    ],
    alpha=0.85
)
# g.set_title('Epidemiological Dynamics - Clinical Incidence of Malaria')
# g.set(xlabel='Time (day)', ylabel='Cases/1000')
rel_times = [730, 737, 744, 751, 758, 765, 772, 779]
for i in rel_times:
    x = ax.axvline(i, alpha=0.5, lw=0.5)
    x.set_zorder(5)
ax.set_aspect(0.15*days/(10))
ax.set_xlim(0, days)
ax.set_ylim(0, 10)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_title("")
ax.get_legend().remove()
plt.show()
g.figure.savefig(
    'clin_inc.tiff', dpi=300,
    transparent=True, bbox_inches='tight', 
    pad_inches=0.1
)