import pandas as pd
import numpy as np
import itertools as iter

'''
This is a short script use the clean up data and create
'''

filename         = 'centrality_data'                                                # File to clean up, assumed to be csv format
data             = pd.read_csv(filename + '.csv')                                   # Read CSV file into DataFrame df
output_file      = 'friendly_centrality'                                            # Define output file

countries        = data['Country'].unique()                                         # Get list of countries
friends_database = pd.DataFrame(columns=['Friend 0', 
                                         'Friend 1', 
                                         'Closeness Friend 0', 
                                         'Betweeness Friend 0', 
                                         'Eigenvector Friend 0', 
                                         'Closeness Friend 1', 
                                         'Betweeness Friend 1', 
                                         'Eigenvector Friend 1', 
                                         '% Diff Closeness', 
                                         '% Diff Betweeness', 
                                         '% Diff Eigenvector',   # Initialize Results Dataframe 
                                         'Data Warning?'])   # Initialize Results Dataframe 

combinations     = list(iter.combinations(countries, 2))                            # Get all combinations of two countries

# For every friend combination
for friends in combinations:

    # Get Data from Friend 0
    Closeness_friend_0   = data[data['Country'] == friends[0]]['Closeness'].values[0]  
    Betweeness_friend_0  = data[data['Country'] == friends[0]]['Betweeness'].values[0]  
    Eigenvector_friend_0 = data[data['Country'] == friends[0]]['Eigenvector'].values[0]  

    # Get Data from Friend 1
    Closeness_friend_1   = data[data['Country'] == friends[1]]['Closeness'].values[0]  
    Betweeness_friend_1  = data[data['Country'] == friends[1]]['Betweeness'].values[0]  
    Eigenvector_friend_1 = data[data['Country'] == friends[1]]['Eigenvector'].values[0]  

    # Find differences
    data_warning = False

    # Closeness    
    if Closeness_friend_0 != 0:
        diff_Closeness_0 = abs(Closeness_friend_0 - Closeness_friend_1) / Closeness_friend_0 * 100
    else:
        diff_Closeness_0 = np.inf
        data_warning = True
        
    if Closeness_friend_1 != 0:
        diff_Closeness_1 = abs(Closeness_friend_1 - Closeness_friend_0) / Closeness_friend_1 * 100
    else:
        diff_Closeness_1 = np.inf
        data_warning = True
        
    # Betweeness    
    if Betweeness_friend_0 != 0:
        diff_Betweeness_0 = abs(Betweeness_friend_0 - Betweeness_friend_1) / Betweeness_friend_0 * 100
    else:
        diff_Betweeness_0 = np.inf
        data_warning = True
        
    if Betweeness_friend_1 != 0:
        diff_Betweeness_1 = abs(Betweeness_friend_1 - Betweeness_friend_0) / Betweeness_friend_1 * 100
    else:
        diff_Betweeness_1 = np.inf
        data_warning = True
        
    # Eigenvector  
    if Eigenvector_friend_0 != 0:
        diff_Eigenvector_0 = abs(Eigenvector_friend_0 - Eigenvector_friend_1) / Eigenvector_friend_0 * 100
    else:
        diff_Eigenvector_0 = np.inf
        data_warning = True
        
    if Eigenvector_friend_1 != 0:
        diff_Eigenvector_1 = abs(Eigenvector_friend_1 - Eigenvector_friend_0) / Eigenvector_friend_1 * 100
    else:
        diff_Eigenvector_1 = np.inf
        data_warning = True
        
    # Store the small diff
    diff_Closeness = min(diff_Closeness_0, diff_Closeness_1)
    diff_Betweeness = min(diff_Betweeness_0, diff_Betweeness_1)
    diff_Eigenvector = min(diff_Eigenvector_0, diff_Eigenvector_1)

    # Calculate friendliness by Multiply them
    
    # If friendship is real, record data
    friendship_entry = {'Friend 0': friends[0],
                        'Friend 1': friends[1], 
                        'Closeness Friend 0': Closeness_friend_0, 
                        'Betweeness Friend 0': Betweeness_friend_0, 
                        'Eigenvector Friend 0': Eigenvector_friend_0, 
                        'Closeness Friend 1': Closeness_friend_1, 
                        'Betweeness Friend 1': Betweeness_friend_1, 
                        'Eigenvector Friend 1': Eigenvector_friend_1, 
                        '% Diff Closeness': diff_Closeness, 
                        '% Diff Betweeness': diff_Betweeness, 
                        '% Diff Eigenvector': diff_Eigenvector,
                        'Data Warning?': data_warning}

    friends_database = friends_database.append(friendship_entry, ignore_index=True)

# Save output to csv file
friends_database.to_csv(output_file + '.csv')