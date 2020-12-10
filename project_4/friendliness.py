import pandas as pd
import numpy as np
import itertools as iter

'''
This is a short script use the clean up data and create
'''

filename         = 'Export_2019_cleanup'                                            # File to clean up, assumed to be csv format
data             = pd.read_csv(filename + '.csv')                                   # Read CSV file into DataFrame df
output_file      = 'friendliness_norm_export_product'                               # Define output file

countries        = data['ReporterISO3'].unique()                                    # Get list of countries
friends_database = pd.DataFrame(columns=['Friend A', 'Friend B', 'Friendliness'])   # Initialize Results Dataframe 

combinations     = list(iter.combinations(countries, 2))                            # Get all combinations of two countries

# For every friend combination
for friends in combinations:

    # Check if there is export data from friend_0 exports to friend_1 
    try:
        friend_0 = data[(data['ReporterISO3'] == friends[0]) & (data['PartnerISO3'] == friends[1])]['Norm_Exports'].values[0]  
    # Else, set it to 1 (ie, other friend decides)
    except:
        friend_0 = 1

    # Check if there is export data from friend_1 exports to friend_0 
    try:
        friend_1 = data[(data['ReporterISO3'] == friends[1]) & (data['PartnerISO3'] == friends[0])]['Norm_Exports'].values[0]  
    # Else, set it to 1 (ie, other friend decides)
    except:
        friend_1 = 1
    
    # Calculate friendliness by Multiply them
    friendliness = friend_0 * friend_1
    
    # If friendliness is 1, then there was no data
    if (friendliness == 1):
        continue

    # If friendship is real, record data
    friendship_entry = {'Friend 0': friends[0],
                        'Friend 1': friends[1], 
                        'Friendliness': friendliness}

    friends_database = friends_database.append(friendship_entry, ignore_index=True)

# Save output to csv file
friends_database.to_csv(output_file + '.csv')