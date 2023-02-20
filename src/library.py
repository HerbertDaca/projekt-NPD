import pandas


def read_data(filename, skiprows):
    return pandas.read_csv(filename, skiprows=skiprows)

def get_min_max_years_from_row(data):
    return[1, 2]

def get_min_max_years_from_column(data):
    return[1, 2]

def adjust_year_range(min_year_1, max_year_1, min_year_2, max_year_2, min_year_3, max_year_3):
    return[max(min_year_1, min_year_2, min_year_3), min(max_year_1, max_year_2, max_year_3)]
