import pandas


def read_data(filename, skiprows):
    return pandas.read_csv(filename, skiprows=skiprows)

def get_min_max_years_from_row(data):
    return [int(data.columns[4]), int(data.columns[-2])]

def get_min_max_years_from_column(data):
    return[data['Year'].min(), data['Year'].max()]

def get_year_range(gdp_data, pop_data, emi_data):
    [gdp_min, gdp_max] = get_min_max_years_from_row(gdp_data)
    [pop_min, pop_max] = get_min_max_years_from_row(pop_data)
    [emi_min, emi_max] = get_min_max_years_from_column(emi_data)
    return[max(gdp_min, pop_min, emi_min), min(gdp_max, pop_max, emi_max)]
