import argparse

import library

parser = argparse.ArgumentParser(description='dependencies between GDP, population and CO2 emission',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('gdp', type=str)
parser.add_argument('population', type=str)                 ## używamy argparse by łatwo przekazać wartości ze zbiorów danych
parser.add_argument('emission', type=str)
parser.add_argument('-start', type=int)
parser.add_argument('-end', type=int)

args = parser.parse_args()

gdp_data = library.read_data(args.gdp, 3)
gdp_data['Country Name'] = gdp_data['Country Name'].str.upper()
pop_data = library.read_data(args.population, 3)
pop_data['Country Name'] = pop_data['Country Name'].str.upper()             ## Nazwy krajów są ponazywane raz samymi wielkimi raz z tylko pierwszą wielką literą. Zmieniamy każdą nazwę kraju na napisaną wielkimi literami.
emi_data = library.read_data(args.emission, 0)

library.clear_data(gdp_data, pop_data)

if args.start and args.end:
    years = list(range(args.start, args.end + 1))                   ## jeśli podane w argparsie są argumenty "start" i "end" to analizujemy dane tylko z przedziału <start, end>
else:
    years = library.get_years_array(gdp_data, pop_data, emi_data)

countries = library.get_countries_array(gdp_data, pop_data, emi_data)       ## Interesują nas kraje, które występują w każdym zbiorze danych więc zbieramy je do tablicy za pomocą "get_countries_array"

merged_array = library.get_merged_data(gdp_data, pop_data, emi_data, years, countries)

library.get_top_five_emissions_per_capita(merged_array)
library.get_top_five_gdp_per_capita(merged_array)

library.get_biggest_difference_in_emission(merged_array, years)
