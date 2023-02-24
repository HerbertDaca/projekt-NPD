import pandas as pd

import numpy

from collections import Counter


def read_data(filename, skiprows):
    return pd.read_csv(filename, skiprows=skiprows)


def get_min_max_years_from_row(data):
    return [int(data.columns[4]), int(data.columns[-1])]


def get_min_max_years_from_column(data):
    return[data['Year'].min(), data['Year'].max()]


def get_years_array(gdp_data, pop_data, emi_data):
    [gdp_min, gdp_max] = get_min_max_years_from_row(gdp_data)           ## pobieramy tylko te lata, które występują we wszystkich zbiorach
    [pop_min, pop_max] = get_min_max_years_from_row(pop_data)
    [emi_min, emi_max] = get_min_max_years_from_column(emi_data)
    return list(range(max(gdp_min, pop_min, emi_min), min(gdp_max, pop_max, emi_max)))


def get_merged_data(gdp_data, pop_data, emi_data, years, countries):
    first_row = True
    for year in years:
        for country in countries:
            gdp = get_gdp_or_population(year, country, gdp_data)
            pop = get_gdp_or_population(year, country, pop_data)
            emi = get_emission(year, country, emi_data)
            if numpy.isnan(gdp):
                continue                                                                                    ## Tutaj jeśli dla któregoś kraju nie znajdziemy w danych wartości dla miary emisji lub miary populacji lub miary gdp
                                                                                                            ## to oznacza, że ten kraj nie występuje we wszystkich zbiorach danych i jego nie bierzemy pod uwagę
            if numpy.isnan(pop):
                continue
            if numpy.isnan(emi):
                continue
            if first_row:
                merged_array = numpy.array([year, country, pop, gdp, gdp/pop, emi, emi/pop])                ## scalamy po latach i krajach czyli tworzymy ramkę, w której dla każdego roku i dla każdego kraju tworzymy osobny wiersz z informacjami, które nas interesują w kolejnych kolumnach
                first_row = False
            else:
                new_row = numpy.array([year, country, pop, gdp, gdp/pop, emi, emi/pop])
                merged_array = numpy.vstack((merged_array, new_row))
    merged_array = pd.DataFrame(merged_array, columns=['year', 'country', 'population', 'gdp', 'gdp_per_capita', 'emission', 'emission_per_capita'])
    merged_array[["emission_per_capita"]] = merged_array[["emission_per_capita"]].astype('float32')
    merged_array[["emission_per_capita"]] = merged_array[["gdp_per_capita"]].astype('float32')
    return merged_array


def get_gdp_or_population(year, country, data):
    cell = data.loc[data['Country Name'] == country, str(year)]             ##funkcja zwraca dla zbioru z populacją dla podanego w argumencie roku i kraju jego populacje czyli odpowiedni wyraz macierzy. robi analogicznie z gdp dla ramki danych gpd
    if cell.count() == 0:
        return numpy.NaN
    return float(cell.item())


def get_emission(year, country, data):
    cell = data.loc[(data['Country'] == country) & (data['Year'] == year), 'Total']         ## dla każdego roku i każdego kraju jest tylko jedna kombinacja ich kombinacja, która da wartość miary emisji.
                                                                                            ## kiedy w wierszu będziemy mieli i (w columnie "Country") kraj zadany argumentem funkcji , (w columnie "Year") i rok zadany argumentem to dostaniemy szukaną miarę emisji tego kraju w tym roku
    if cell.count() == 0:
        return numpy.NaN
    return float(cell.item())


def get_countries_array(gdp_data, pop_data, emi_data):
    gdp_countries = gdp_data['Country Name'].to_numpy().astype(str)
    pop_countries = pop_data['Country Name'].to_numpy().astype(str)
    emi_countries = numpy.unique(numpy.array(emi_data['Country']))
    countries = numpy.unique(numpy.hstack((gdp_countries, pop_countries, emi_countries)))   ## bierzemy sumę wszystkich trzech zbiorów krajów z każdej bazy danych, chciało by się by
                                                                                            ## były to kraje, które są w każdym zbiorze danych jednocześnie, ale ten problem jest załatwiany w "get_merged_data()".
    return countries


def clear_data(gdp_data, pop_data):
    gdp_data = gdp_data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1)
    pop_data = pop_data.drop(['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1)       ##niepotrzeba tych kolumn czyszczenie danych
    return gdp_data, pop_data


def get_top_five_emissions_per_capita(merged_data):
    print('\nFive countries with largest emission per capita\n')
    print(merged_data.sort_values(by='emission_per_capita', ascending=False)[['year', 'country', 'emission', 'emission_per_capita']].head(5))       ## żeby wykonać pierwsze zadanie należy posortować malejąco względem emisji per capita i wziąć pierwsze 5


def get_top_five_gdp_per_capita(merged_data):
    print('\nFive countries with largest gdp per capita\n')
    print(merged_data.sort_values(by='gdp_per_capita', ascending=False)[['year', 'country', 'gdp', 'gdp_per_capita']].head(5))                      ## żeby wykonać drugie zadanie należy posortować malejąco względem gdp per capita i wziąć pierwsze 5

def get_biggest_difference_in_emission(merged_data, years):
    emission_now = merged_data.loc[merged_data['year'] == str(years[-1])][['country', 'emission_per_capita']]                                       ## szukamy w scalonych danych lokalizacji emisji per kapita z ostatniego roku i przypisujemy zlokalizowaną wartość tej emisji do zmiennej
    emission_ten_years_ago = merged_data.loc[merged_data['year'] == str(years[-1] - 10)][['country', 'emission_per_capita']]                        ##  szukamy w scalonych danych lokalizacji emisji per kapita z roku 10 lat starszego od ostatniego w liście wszystkich i przypisujemy zlokalizowaną wartość  do zmiennej
    countries_ten_years_ago = numpy.unique(numpy.array(emission_ten_years_ago['country']))
    countries_now = numpy.unique(numpy.array(emission_now['country']))                                                                              ## Weźmy wszystkie kraje, które mierzyły emisję w ostatnim roku
    countries = numpy.hstack((countries_ten_years_ago, countries_now))                                                                              ## Weźmy wszystkie kraje, które mierzyły emisje w roku 10 lat starszym od ostatniego roku
    countries = [item for item, count in Counter(countries).items() if count > 1]
    emission_ten_years_ago = emission_ten_years_ago[emission_ten_years_ago['country'].isin(countries)]
    emission_now = emission_now[emission_now['country'].isin(countries)]
    emission_now[["emission_per_capita"]] = emission_now[["emission_per_capita"]].astype('float32')
    emission_ten_years_ago[["emission_per_capita"]] = emission_ten_years_ago[["emission_per_capita"]].astype('float32')
    emission_comparison = emission_now.set_index('country').subtract(emission_ten_years_ago.set_index('country'))
    emission_comparison = emission_comparison.sort_values(by='emission_per_capita', ascending=False)
    print('\nSmallest increase in emission per capita in 10 years\n')
    print(emission_comparison.tail(1))
    print('\nBiggest increase in emission per capita in 10 years\n')
    print(emission_comparison.head(1))
