import os
import csv
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx


def visualize_graph(G, with_world_map = True):
    
    if with_world_map:
        
        m = bm.Basemap(width=5.e6, height=3.e6, projection='cyl', lat_0=0, lon_0=0)
        
        m.drawcoastlines(linewidth=0.5)
        m.drawmapboundary(fill_color='whitesmoke', linewidth=0.5)
        m.fillcontinents(color='white', lake_color='whitesmoke')
        m.drawcountries(linewidth=0.5)
        m.drawstates(linewidth=0.5)
        
        lats = [coord[0] for coord in coords]
        lons = [coord[1] for coord in coords]
        
        py, px = m(lats, lons)
        pos = zip(px, py)
        layout = dict(zip(G, pos))
        
        regulating_constant = 1e3
        node_sizes = [(cases/population)*regulating_constant for (cases, population) in zip(covid_cases, populations)]
        nx.draw_networkx(G, pos=layout, width=1.0, node_size=node_sizes, node_color=colors, edge_color='red', with_labels=False)
        
    else:
        regulating_constant = 3e4
        node_sizes = [(cases/population)*regulating_constant for (cases, population) in zip(covid_cases, populations)]
        nx.draw_networkx(G,width=1.0, node_size=node_sizes)
    
    plt.show()





# this line solves bug related to PROJ_LIB
#os.environ['PROJ_LIB'] = "C:\\ProgramData\\Anaconda3\\Library\\share"

# Federico: Custom change. Using an Ubuntu pc.
os.environ['PROJ_LIB'] = "/home/fico/anaconda3/share/proj/"

import mpl_toolkits.basemap as bm

# get list of files with trade info from country_files_detailed_summary folder
country_files = os.listdir(os.getcwd()+'/'+'country_files_detailed_summary')
country_files = ['country_files_detailed_summary/' + file_name for file_name in country_files]

# create graph
G = nx.DiGraph()

# create countries lists
relevant_countries = ['Argentina', 'Belgium', 'Brazil', 'Chile', 'Colombia', 'Czech Republic', 'France', 'Netherlands', 'Peru', 'Spain', 'United Kingdom', 'United States']
relevant_countries = ['ARG', 'BEL', 'BRA', 'CHI', 'COL', 'CZR', 'FRA', 'NET', 'PER', 'SPA', 'UK', 'US']

# countries values follow the same order as relevant_countries list
covid_cases = [1.24e6, 494e3, 5.65e6, 522e3, 1.14e6, 411e3, 1.79e6, 410e3, 918e3, 1.33e6, 1.19e6, 10e6]
#populations = {'Argentina':44.49e6, 'Belgium':11.46e6, 'Brazil':209.5e6, 'Chile':18.73e6, 'Colombia':49.65e6, 'Czech Republic':10.65e6, 'France':66.99e6, 'Netherlands':17.28e6, 'Peru':31.99e6, 'Spain':46.94e6, 'United Kingdom':66.65e6, 'United States':328.2e6}
populations = [44.49e6, 11.46e6, 209.5e6, 18.73e6, 49.65e6, 10.65e6, 66.99e6, 17.28e6, 31.99e6, 46.94e6, 66.65e6, 328.2e6]

coords = [[-38.4161, -63.6167], [50.50389, 4.469936], [-14.235, -51.9253], [-35.6751, -71.543], [4.570868, -74.2973], [49.817492, 15.472962], [46.227638, 2.213749], [52.132633, 5.291266], [-9.189967, -75.015152], [40.463667, -3.74922], [55.378051, -3.435973], [37.09024, -95.712891]]
colors = ['blue', 'cyan', 'blue', 'blue', 'blue', 'blue', 'black', 'yellow', 'blue', 'green', 'blue', 'blue']

# add nodes
G.add_nodes_from(relevant_countries)


for i in range(len(country_files)): # for each file    
    with open(country_files[i], encoding="utf-8") as file: # open file
        
        reader = csv.reader(file, delimiter=',')
        headers = next(reader, None) # ignore headers
        
      
        for row in reader: # for each row
        
            # if countries in relation are in relevant_countries
            if row[0] in relevant_countries and row[1] in relevant_countries: 
                
                if row[3] == 'Export': # if relation is export, add edge country_0 -> country_1
                    G.add_edge(row[0], row[1])
                    print(row[0], '-->' ,row[1]) 
                    
                elif row[3] == 'Import': # if relation is export, add edge country_1 -> country_0
                    G.add_edge(row[1], row[0])
                    print(row[1], '-->' ,row[0])


visualize_graph(G, False)
