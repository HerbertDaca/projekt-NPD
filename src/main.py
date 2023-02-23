import argparse

import library

import numpy


parser = argparse.ArgumentParser(description='dependencies between GDP, population and CO2 emission',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('gdp', type=str)
parser.add_argument('population', type=str)
parser.add_argument('emission', type=str)
parser.add_argument('-start', type=int)
parser.add_argument('-end', type=int)

args = parser.parse_args()

gdp_data = library.read_data(args.gdp, 3)
gdp_data['Country Name'] = gdp_data['Country Name'].str.upper()
pop_data = library.read_data(args.population, 3)
pop_data['Country Name'] = pop_data['Country Name'].str.upper()
emi_data = library.read_data(args.emission, 0)

library.clear_data(gdp_data, pop_data)

if args.start and args.end:
    years = list(range(args.start, args.end + 1))
else:
    years = library.get_years_array(gdp_data, pop_data, emi_data)

# print(years)
countries = library.get_countries_array(gdp_data, pop_data, emi_data)

merged_array = library.get_merged_data(gdp_data, pop_data, emi_data, years, countries)

# top_five_not_eco = library.get_top_five_not_eco_nations(merged_array)
library.get_top_five_emissions_per_capita(merged_array)
library.get_top_five_gdp_per_capita(merged_array)


# data.columns = data.columns.astype("str")
