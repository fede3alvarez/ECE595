import csv
from scipy import stats
from sklearn import preprocessing as pp
import os
import matplotlib.pyplot as plt
import math

import networkx as nx


# final plot growth rate correlation vs friendliness
def plot_growth_corr_x_friendl(growth_corr_list, friendl_list):
    
    
    if len(growth_corr_list) != len(friendl_list):
        return 
    
    plt.xlabel('average growth rates correlation')
    plt.ylabel('friendliness')
    
    #plt.ylim(0, 0.2)
    
    for i in range(len(growth_corr_list)):    
        #if friendl_dict[key] == 0:
        #    continue
        corr = growth_corr_list[i] 
        friendl = friendl_list[i]
        
        plt.scatter(corr, friendl, marker='o', color='blue')
        
    print(stats.pearsonr(growth_corr_list, friendl_list))
    plt.show()
    
    
# this function is used to ensure consistency for countries with different names in different datasets
def convert_country_short(country):
    if country == 'Russian Federation':
        return 'Russia'
    elif country == 'Iran, Islamic Rep.':
        return 'Iran'
    else:
        return country

# this function is used to ensure consistency for countries with different names in different datasets
def convert_countries_long(relevant_countries):
    new_relevant_countries = [] 
    
    for i in range(len(relevant_countries)):
        if relevant_countries[i] == 'Russia':
            new_relevant_countries.append('Russian Federation')
        elif relevant_countries[i] == 'Iran':
            new_relevant_countries.append('Iran, Islamic Rep.')
        else:
            new_relevant_countries.append(relevant_countries[i])
    
    return new_relevant_countries
        
# calculate growth rate between two days
def calc_growth_rate(v_prev, v):
    #STANDARD_VALUE_TO_AVOID_DIVISION_BY_ZERO = 1e-3    
    
    if v_prev == 0 and v == 0:
        return 0
    
    if v_prev == 0 and v != 0:
        return v
    
    return (v - v_prev)/v_prev
    #return (v - v_prev)

# calculate avg growth rate from list of values
def calc_avg_growth_rate(cases_list):
    N = len(cases_list)
    summ_growth_rates = 0
    for i in range(1, N):
        summ_growth_rates += calc_growth_rate(cases_list[i-1], cases_list[i])     
    
    avg_growth_rate = summ_growth_rates/N
    return avg_growth_rate


# calculate list of avg growth rates bases on window_size
def gen_growth_rates(dates_cases_dict, window_size = 7):
    dates_cases_list = list(dates_cases_dict.values())
    growth_rates = []
    for i in range(window_size+1, len(dates_cases_dict)):
        
        growth_rates.append(calc_avg_growth_rate(dates_cases_list[i-window_size: i]))    
    return growth_rates


# get daily per-country covid data from file
with open('owid-covid-data.csv') as file:
    reader = csv.reader(file, delimiter=',')
    headers = next(reader, None) # ignore headers
    
    countries_dates_cases_dict = {}

    for line in reader:
                
        if line[2] in ('World','Hong Kong') or line[3] < '2020-01-23':
            continue
        
        if line[2] not in countries_dates_cases_dict:
            countries_dates_cases_dict[line[2]] = {}
        
        if line[4] == '':
            countries_dates_cases_dict[line[2]][line[3]] = 0
        else:
            countries_dates_cases_dict[line[2]][line[3]] = float(line[4])
     
        
# define relevant countries for the experiment
relevant_countries = ['Czech Republic', 'Belgium', 'United States', 'Spain', 'France'\
                      , 'Netherlands', 'Argentina', 'Portugal', 'Brazil', 'Peru'\
                          , 'Sweden', 'Chile', 'Italy', 'Poland', 'Romania', 'Colombia'\
                              , 'United Kingdom', 'Jordan', 'Ukraine', 'Russia', 'Azerbaijan'\
                                  , 'Germany', 'Iraq', 'South Africa', 'Dominican Republic'\
                                      , 'Iran', 'Bolivia', 'Greece', 'Canada', 'Ecuador'\
                                          , 'Turkey', 'Morocco', 'Saudi Arabia']

relevant_countries.sort()
####################################################################################
# growth rate correlations between pairs of countries
countries_growth_rates = {}
for key in countries_dates_cases_dict:
    if key not in relevant_countries:
        continue
    
    # change window_size in function call below accordingly
    countries_growth_rates[key] = [key]
    countries_growth_rates[key].extend(gen_growth_rates(countries_dates_cases_dict[key], window_size = 7))


# calculate both pearson and spearman correlations between every pair of countries
corr_coefs_dict = {}
corr_headers = [['countries','pearson corr','pearson p']]

for i in range(len(countries_growth_rates)):
    key_i = list(countries_growth_rates.keys())[i]
    for j in range(i+1,len(countries_growth_rates)):
        key_j = list(countries_growth_rates.keys())[j]
        pearson_coef, pearson_p = stats.pearsonr(countries_growth_rates[key_i][1:]\
                                                 , countries_growth_rates[key_j][1:])
        
        spearman_coef, spearman_p = stats.spearmanr(countries_growth_rates[key_i][1:]\
                                                 , countries_growth_rates[key_j][1:])
            
        #corr_coefs_dict[key_i + '_' + key_j] = [key_i + '_' + key_j, pearson_coef, pearson_p, spearman_coef, spearman_p]
        corr_coefs_dict[key_i + '_' + key_j] = pearson_coef
##########################################################################################
# friendliness between pairs of countries       
        
# get list of files with trade info from trade_2019_cleanup.csv file
with open('trade_2019_cleanup.csv') as file:
    reader = csv.reader(file, delimiter=',')
    headers = next(reader, None) # ignore headers
    
    countries_trades_dict = {}
    countries_populations_dict = {}
    
    for row in reader:
        if row[5] in convert_countries_long(relevant_countries)\
            and row[7] in convert_countries_long(relevant_countries):
                new_key = ''
                                
                if convert_country_short(row[5])+'_'+convert_country_short(row[7]) in corr_coefs_dict:
                    new_key = convert_country_short(row[5])+'_'+convert_country_short(row[7])
                elif convert_country_short(row[7])+'_'+convert_country_short(row[5]) in corr_coefs_dict:
                    new_key = convert_country_short(row[7])+'_'+convert_country_short(row[5])
                
                # total trade between country A and B defined as export(A,B) + export(B,A)
                if new_key != '':
                    if new_key not in countries_trades_dict:
                        countries_trades_dict[new_key] = float(row[12])
                    else:
                        countries_trades_dict[new_key] += float(row[12])
                    #countries_populations_dict[new_key] = populations[convert_country_short(row[5])] + populations[convert_country_short(row[7])]

# friendliness between country A and B define as (export(A,B) + export(B,A)) / 2
countries_friendl_dict = {}
for key in countries_trades_dict:
    #countries_friendl_dict[key] =  math.sqrt(1 + 1e8*(countries_trades_dict[key] / (2*countries_populations_dict[key])))
    countries_friendl_dict[key] =  (countries_trades_dict[key] / 2)

# give friendliness value of zero for countries that do not trade
for key in corr_coefs_dict:
    if key not in countries_friendl_dict:
        countries_friendl_dict[key] = 0
        
corr_coefs_list = list(corr_coefs_dict.values())
countries_friendl_list = list(countries_friendl_dict.values())   

# plot 
plot_growth_corr_x_friendl(corr_coefs_list, countries_friendl_list)


'''
G = nx.Graph()

for key in corr_coefs_dict:
    key_split = key.split('_') 
    print(key_split)
    print(corr_coefs_dict[key][1])
    G.add_edge(key_split[0], key_split[1], correlation = corr_coefs_dict[key][1])
'''       
###############################################################


'''
with open('correlations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    corr_coefs = list(corr_coefs_dict.values())
    
    writer.writerows(corr_headers)
    writer.writerows(corr_coefs)
'''

'''
with open('growth_rates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    countries_growth_rates = list(countries_growth_rates.values())
    
    writer.writerows(countries_growth_rates)
'''

'''
with open('relevant_countries.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    relevant_countries_column = []
    for i in range(len(relevant_countries)):
        relevant_countries_column.append([relevant_countries[i]])
    
    writer.writerows(relevant_countries_column)
'''