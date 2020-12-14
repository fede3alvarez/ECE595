import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get Data, and set process per country
df = pd.read_csv (r'data_cleaned_up.csv')
df = df[df['7d total norm. per'].notna()]
df['date'] = pd.to_datetime(df['date'])
countries = pd.unique(df['location'])

row = 0
col = 0

# Iterate per Country and plot desired data
for country in countries:
    country_data = df[df['location'] == country]
    country_data = country_data.sort_values('date', ascending=True)
    country_data.to_csv(country+'.csv', index = True) 



'''
plt.xticks(rotation='vertical')
plt.show()
# Reduce number of ticks pn y axis
every_nth = 10
for n, label in enumerate(ax.yaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
    print(country_data['7d total norm. per'])
    print("------------------------")

    plt.savefig('my_figure.png')
    plt.plot(x, y)

fig, axs = plt.subplots(6, 2)
axs[0, 0].plot(x, y)
axs[0, 0].set_title('Axis [0,0]')
axs[0, 1].plot(x, y, 'tab:orange')
axs[0, 1].set_title('Axis [0,1]')
axs[1, 0].plot(x, -y, 'tab:green')
axs[1, 0].set_title('Axis [1,0]')
axs[1, 1].plot(x, -y, 'tab:red')
axs[1, 1].set_title('Axis [1,1]')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
'''