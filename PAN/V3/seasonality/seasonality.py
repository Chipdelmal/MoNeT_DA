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
ax = sns.scatterplot(data=df_rain, x="day_of_year", y="rainfall", s=5)
ax.set(xlabel='Day of Year', ylabel='Rainfall (mm)', title='Seasonality - São Tomé and Príncipe')
plt.plot(df_prof['x'], color=palette.as_hex()[-1])
plt.savefig('seasonality.tiff', dpi=300)
plt.show()
# %%

# %%
