import csv
import matplotlib.pyplot as plt
from scipy import stats

#
def plot_pair_of_g_rates(country_a_g_rates, country_b_g_rates):
    if len(country_a_g_rates) != len(country_a_g_rates):
        return 
    
    plt.xlabel(country_a_g_rates[0])
    plt.ylabel(country_b_g_rates[0])
    for i in range(1, len(country_a_g_rates)):    
        plt.scatter(country_a_g_rates[i], country_b_g_rates[i], marker='o', color='blue')
    
    # slice starting at 1 to ignore country names
    pearson_coef, pearson_p = stats.pearsonr(country_a_g_rates[1:],country_b_g_rates[1:])
    spearman_coef, spearman_p = stats.spearmanr(country_a_g_rates[1:],country_b_g_rates[1:])
    
    pearson_coef_str = str.format('%.2f' %pearson_coef)
    spearman_coef_str = str.format('%.2f' %spearman_coef) 
    
    plt.title('Covid moving growth rates\n7 day window avg\n'\
              +'pearson='+str(pearson_coef_str)+' '+'spearman='+str(spearman_coef_str))
    plt.show()


# open file and collect data in variable dictionary countries_growth_rates_dict
# each key connects to a list where the country name is at position 0
with open('growth_rates.csv') as file:
    reader = csv.reader(file, delimiter=',')
        
    countries_growth_rates_dict = {}

    for line in reader:
        countries_growth_rates_dict[line[0]] = [line[0]]
        countries_growth_rates_dict[line[0]].extend([float(value) for value in line[1:]])
        
 
##################################################################################
### Place the countries to be studied in the list relevant_countries

relevant_countries = ['Czech Republic', 'Belgium', 'United States', 'Spain', 'France', 'Netherlands', 'Argentina', 'Portugal', 'Brazil', 'Peru', 'Sweden', 'Chile', 'Italy', 'Poland', 'Romania', 'Colombia', 'United Kingdom', 'Jordan', 'Ukraine', 'Russia', 'Azerbaijan', 'Germany', 'Iraq', 'South Africa', 'Dominican Republic', 'Iran', 'Bolivia', 'Greece', 'Canada', 'Ecuador', 'Turkey', 'Morocco', 'Saudi Arabia']
N = len(relevant_countries)

'''
# check if all relevant countries are in dictionary
for i in range(N):
    if relevant_countries[i] not in countries_growth_rates_dict:
        print('country', relevant_countries[i], 'not in dict')
'''


### Change to decide regulate which countries to check
# Please uncomment the part directly below your name

# Federico - 177 pairs of countries
country_begin_i = 0
country_end_i = 6



# Mauricio - 180 pairs of countries
#country_begin_i = 6
#country_end_i = 14


# Stephan - 171 pairs of countriw
#country_begin_i = 14
#country_end_i = N


count = 0
for i in range(country_begin_i, country_end_i):
    for j in range(i + 1, N):
        plot_pair_of_g_rates(countries_growth_rates_dict[relevant_countries[i]]\
                             ,countries_growth_rates_dict[relevant_countries[j]])
        count += 1
        print(count)

