import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
This is a short script to plot data

x = spearman coefficient
y = friendliness
'''

filename  = 'Test_data'                                            # File to clean up, assumed to be csv format
data      = pd.read_csv(filename + '.csv')                                   # Define output file

#countries = data['ReporterISO3'].unique()                                    # Get list of countries

# 'spearman corr'   'Friendliness'
# 'SOUTH AMERICA'   'EUROPE'  'USA'   'Not FRIEND'
#x_south_america  = data[(data['SOUTH AMERICA'] == 'TRUE')]['spearman corr']  
x_south_america  = data[(data['SOUTH AMERICA'] == True)]['spearman corr']
y_south_america  = data[(data['SOUTH AMERICA'] == True)]['Friendliness']

x_europe  = data[(data['EUROPE'] == True)]['spearman corr']
y_europe  = data[(data['EUROPE'] == True)]['Friendliness']

x_usa  = data[(data['USA'] == True)]['spearman corr']
y_usa  = data[(data['USA'] == True)]['Friendliness']

x_not_friends  = data[(data['Not FRIEND'] == True)]['spearman corr']
y_not_friends  = data[(data['Not FRIEND'] == True)]['Friendliness']

# Plot
plt.scatter(x_south_america, y_south_america,label='Sout America', color='g')
plt.scatter(x_europe, y_europe,label='Europe', color='b')
plt.scatter(x_usa, y_usa,label='USA', color='r')
plt.scatter(x_not_friends, y_not_friends,label='Not friendly', color='k')
#plt.xscale("log")
plt.yscale("log")
plt.show()