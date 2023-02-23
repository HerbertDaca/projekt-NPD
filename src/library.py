import pandas as pd
import numpy


def read_data(filename, skiprows):
    return pd.read_csv(filename, skiprows=skiprows)


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
    first_row = True
    # data_type = [('year',int),('country',str),('population',int),('gdp',float),('gdp_per_capita',float),('emission',int),('emission_per_capita',float)]
    merged_array = pd.DataFrame()
    for year in years:
        for country in countries:
            gdp = get_gdp_or_population(year, country, gdp_data)
            pop = get_gdp_or_population(year, country, pop_data)
            emi = get_emission(year, country, emi_data)
            if numpy.isnan(gdp):
                continue
            if numpy.isnan(pop):
                continue
            if numpy.isnan(emi):
                continue
            # if first_row:
            #     # merged_array = numpy.array((year, country, pop, gdp, gdp/pop, emi, emi/pop), dtype = data_type)
            #     first_row = False
            # else:
            new_row = pd.DataFrame((year, country, pop, gdp, gdp/pop, emi, emi/pop))
            merged_array.append(new_row)

    return merged_array


def get_gdp_or_population(year, country, data):
    cell = data.loc[data['Country Name'] == country, str(year)]
    if cell.count() == 0:
        return numpy.NaN
    return float(cell.item())


def get_emission(year, country, data):
    cell = data.loc[(data['Country'] == country) & (data['Year'] == year), 'Total']
    if cell.count() == 0:
        return numpy.NaN
    return float(cell.item())


def get_countries_array(gdp_data, pop_data, emi_data):
    gdp_countries = gdp_data['Country Name'].to_numpy().astype(str)
    pop_countries = pop_data['Country Name'].to_numpy().astype(str)
    emi_countries = numpy.unique(numpy.array(emi_data['Country']))
    countries = numpy.unique(numpy.hstack((gdp_countries, pop_countries, emi_countries)))
    return countries


def clear_data(gdp_data, pop_data):
    gdp_data = gdp_data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1)
    pop_data = pop_data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1)
    return gdp_data, pop_data


# def get_top_five_not_eco_nations(merged_data):
    # merged_data[-5:-1, :].sort(order=merged_data, kind='heapsort', axis=0)
    # data_type = [('year', int), ('country', numpy.unicode, 20), ('population', int), ('gdp', float), ('gdp_per_capita', float), ('emission', int), ('emission_per_capita', float)]

    # merged_data = pd.DataFrame(merged_data, index=data_type)
    # top_five_not_eco = numpy.sort(merged_data, order='emission_per_capita')
