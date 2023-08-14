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

# extract labels for prevalence states
labels = "^clin_inc"
time = df['Time']
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
STP_pop = 223000
clininc_df = pd.DataFrame()
for idx in age_idx.keys():
    clininc_df[age_idx[idx]] = df.filter(
        regex=idx).sum(axis=1) * (STP_pop/1000)

clininc_df['All-ages'] = clininc_df.sum(axis=1)
clininc_df['Time'] = time

# Remove weird dynamics at t=0
clininc_df.iloc[0] = None

# scale by population/1000

clininc_df_melt = clininc_df.melt('Time', var_name='cols', value_name='vals')
clininc_df_melt.rename(columns={'cols': 'Age Group (yrs)'}, inplace=True)
fig, ax = plt.subplots(figsize=(20,6))
g = sns.lineplot(x="Time", y="vals", hue='Age Group (yrs)', data=clininc_df_melt)
g.set_title('Epidemiological Dynamics - Clinical Incidence of Malaria')
g.set(xlabel='Time (day)', ylabel='Cases/1000')
rel_times = [730, 737, 744, 751, 758, 765, 772, 779]
for i in rel_times:
    x = g.axvline(i, alpha=0.2)
    x.set_zorder(0)

g.figure.savefig('clin_inc.tiff', dpi=300)


