

# Plot allele frequency for TP13 in STP
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

palette = sns.color_palette("icefire")
sns.set(font='Arial', font_scale=0.80)
sns.set_palette(palette)
sns.set_style('ticks')

# read in data
df_female = pd.read_csv("F_Mean_0001.csv")
days = df_female.shape[0]

# Convert genotypes to alleles


# rescale so everything is in terms of frequency
time = df_female['Time']
df_female = df_female.drop('Time', axis=1)

df_female_allele = pd.DataFrame()
df_female_allele['H*'] = df_female['BH'] + df_female['HH'] + df_female['HR'] + df_female['HW']
df_female_allele['Other'] = df_female['BB'] + df_female['BR'] + df_female['BW'] + df_female['RR'] + df_female['RW'] + df_female['WW']



df_female_allele = df_female_allele.div(df_female_allele.sum(axis=1), axis=0)

# Convert to long format
df_female_allele['Time'] = time
df_female_allele = df_female_allele.melt('Time', var_name='cols', value_name='vals')
df_female_allele.rename(columns={'cols': 'Allele Frequency'}, inplace=True)


# Plot
(fig, axes) = plt.subplots(figsize=(20,6))
rel_times = [730, 737, 744, 751, 758, 765, 772, 779]
g = sns.lineplot(
    ax=axes, x="Time", y="vals", 
    hue='Allele Frequency', data=df_female_allele,
    lw=2.5, alpha=0.75
)
for i in rel_times:
    x = axes.axvline(i, alpha=0.5, lw=1)
    x.set_zorder(0)
# fig.suptitle('Entomological Dynamics - Allele Frequency')
# axes.set_title('Female Mosquitoes')
# axes.set(xlabel='Time (day)', ylabel='Allele frequency')
axes.set_aspect(0.15*days/1.25)
axes.set_xlim(0, days)
axes.set_ylim(0, 1.25)
axes.set_xticks([])
axes.set_yticks([])
axes.set_xlabel("")
axes.set_ylabel("")
axes.get_legend().remove()

# save
g.figure.savefig(
    'allele_freq.tiff', dpi=300,
    transparent=True, bbox_inches='tight', 
    pad_inches=0.1
)

# %%
