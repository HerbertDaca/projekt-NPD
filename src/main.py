import argparse

import pandas

import library


parser = argparse.ArgumentParser(description='zaleznosci miedzy dochodami panstw, liczbami mieszkancow i emisja CO2',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('gpd', type=str)
parser.add_argument('population', type=str)
parser.add_argument('emission', type=str)

args = parser.parse_args()


gpd_data = library.read_data(args.gpd, 3)
pop_data = library.read_data(args.population, 3)
emi_data = library.read_data(args.emission, 0)

print(library.get_min_max_years_from_row(gpd_data))
print(library.get_min_max_years_from_row(pop_data))
print(library.get_min_max_years_from_column(emi_data))

print(library.get_year_range(gdp_data=gpd_data, pop_data=pop_data, emi_data=emi_data))

# print(library.get_min_max_years_from_row(gpd_data))
# print(library.get_min_max_years_from_row(cit_data))
# print(library.get_min_max_years_from_column(emi_data))

# data.columns = data.columns.astype("str")
# pandas.options.display.float_format = '{:.2f}'.format
