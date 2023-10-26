# %%

# Plot seasonality profile and daily rainfall for STP

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

palette = sns.light_palette("seagreen")
sns.set(font='Arial', font_scale=0.80)
sns.set_palette(palette)
sns.set_style('ticks')

# %%
df_rain = pd.read_csv('rainfall_stp.csv')
df_prof = pd.read_csv('profile_stp.csv')


(fig, ax) = plt.subplots(figsize=(20,6))
# ax = sns.scatterplot(
#     data=df_rain, x="day_of_year", y="rainfall", s=5,
#     palette='#000000'
# )
ax.scatter(
    df_rain['day_of_year'], df_rain['rainfall'],
    marker='x', color='#788bff22', zorder=-1
)
# ax.set(
#     xlabel='Day of Year', ylabel='Rainfall (mm)', 
#     title='Seasonality - São Tomé and Príncipe'
# )
ax.plot(
    df_prof['x'], #color=palette.as_hex()[-1]
    color='#3d5a8088', lw=5, zorder=10
)
plt.yscale('symlog')
ticks = [0, 1, 5, 10, 25, 50, 100, 200]
ax.set_yticks(ticks, labels=[]) #ticks)
# ax.set_xticks(range(0, 365, int(365/5)))
ax.set_xticklabels([])
ax.set_ylim(0, 200)
ax.set_xlim(0, 365)
fig.savefig(
    'seasonality.tiff', dpi=300,
    transparent=True, bbox_inches='tight', 
    pad_inches=0.1
)

# %%

# %%
