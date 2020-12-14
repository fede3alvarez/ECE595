import os
import csv
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx

'''
This script use the clean export data with the networkx library to obtain centrality values
'''

# The next line solves bug related to PROJ_LIB
# See link for details: https://community.dataquest.io/t/cant-install-basemap/7542/4

# Windows 
# os.environ['PROJ_LIB'] = "C:\\ProgramData\\Anaconda3\\Library\\share"

# Custom change. Using an Ubuntu pc.
os.environ['PROJ_LIB'] = "/home/fico/anaconda3/share/proj/"

import mpl_toolkits.basemap as bm


filename = 'Export_2019_cleanup'
data = pd.read_csv(filename + '.csv') 

# Use Pandas dataframe to populate the directed network values
G = nx.from_pandas_edgelist(data, 'ReporterISO3', 'PartnerISO3', ['Norm_Exports'], create_using=nx.DiGraph())

# Compute Centralities
world_closeness   = nx.closeness_centrality(G)
world_betweenness = nx.betweenness_centrality(G)
world_eigenvector = nx.eigenvector_centrality(G)

countries  = data['ReporterISO3'].unique()  # Get list of countries
centrality_data = pd.DataFrame()

for country in countries:
    country_entry = {'Country': country,
                     'Closeness': world_closeness.get(country), 
                     'Betweeness': world_betweenness.get(country), 
                     'Eigenvector': world_eigenvector.get(country)}

    centrality_data = centrality_data.append(country_entry, ignore_index=True)

centrality_data = centrality_data[['Country', 'Closeness', 'Betweeness', 'Eigenvector']]

print(centrality_data)
centrality_data.to_csv('centrality_data.csv')