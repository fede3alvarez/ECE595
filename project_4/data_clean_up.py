import pandas as pd
import numpy as np

'''
This is a short script to clean up the downloaded data and normalized exports
'''

filename = 'Export_2019'                    # File to clean up, assumed to be csv format
output_file = filename + '_cleanup'         # Output file

data = pd.read_csv(filename + '.csv')       # Read CSV file into DataFrame df
data['Norm_Exports'] = 0                    # Create a new entry / column & Initialize it to zero

countries  = data['ReporterISO3'].unique()  # Get list of countries

# Update each country with normalized data
for country in countries:

    # Get total exports for current country
    total = data[(data['ReporterISO3'] == country) & (data['PartnerISO3'] == 'WLD')]['TradeValue in 1000 USD'].values[0]   

    # Update Column 'Norm_Exports' =  'TradeValue in 1000 USD' / total
    data.loc[data['ReporterISO3'] == country,'Norm_Exports'] = data.loc[data['ReporterISO3'] == country,'TradeValue in 1000 USD']  / total

# Remove export to 'Unspecified'
# Otherwise 'Unspecified' may display as a friendly new World Power
data.drop(data[data['PartnerName'] == 'Unspecified' ].index , inplace=True)
#data = countries[countries != country]

# Save output to csv file
data.to_csv(output_file + '.csv')