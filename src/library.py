import pandas
import numpy


def read_data(filename, skiprows):
    return pandas.read_csv(filename, skiprows=skiprows)

def get_min_max_years_from_row(data):
    return [int(data.columns[4]), int(data.columns[-2])]

def get_min_max_years_from_column(data):
    return[data['Year'].min(), data['Year'].max()]

def get_years_array(gdp_data, pop_data, emi_data):
    [gdp_min, gdp_max] = get_min_max_years_from_row(gdp_data)
    [pop_min, pop_max] = get_min_max_years_from_row(pop_data)
    [emi_min, emi_max] = get_min_max_years_from_column(emi_data)
    return list(range(max(gdp_min, pop_min, emi_min), min(gdp_max, pop_max, emi_max)))

def get_merged_data(gdp_data, pop_data, emi_data, years, countries):
    for year in years:
        for country in countries:
            gdp = get_gdp_or_population(year, country, gdp_data, 'GDP')
            pop = get_gdp_or_population(year, country, pop_data, 'population')
            new_row = [year, country, pop, gdp, gdp/pop, '', '']
            if gdp.count() != 0:
                print(gdp.item)
                print(float(gdp))
            merged_array = numpy.append(merged_array, [year, country, ])
    merged_dataframe = 0
    return merged_dataframe

def get_gdp_or_population(year, country, data, data_caption):
    cell = data.loc[data['Country Name'] == country, str(year)]
    if cell.count() == 0:
        print(country + ' could not be found in ' + data_caption + ' data.')
        return numpy.Nan
    return float(cell.item)

def get_emission(year, country, data):
    return 0

def get_countries_array(gdp_data, pop_data, emi_data):
    gdp_countries = gdp_data['Country Name'].to_numpy().astype(str)
    pop_countries = pop_data['Country Name'].to_numpy().astype(str)
    emi_countries = numpy.unique(numpy.array(emi_data['Country']))
    countries = numpy.unique(numpy.hstack((gdp_countries, pop_countries, emi_countries)))
    return countries
