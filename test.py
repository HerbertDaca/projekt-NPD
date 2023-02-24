import unittest

import pandas as pd

import src.library


class Test(unittest.TestCase):
    def test_get_years_array(self):
        data = {'Country Name': ['Test'],
                'Country Code': ['TST'],
                'Indicator Name': ['test'],
                'Indicator Code': ['test'],
                '2000': [1],
                '2001': [1],
                '2002': [1],
                '2003': [1],
                '2004': [1],
                '2005': [1],
                '2006': [1],
                '2007': [1],
                '2008': [1],
                '2009': [1],
                '2010': [1]}
        df1 = pd.DataFrame(data)
        data = {'Country Name': ['Test'],
                'Country Code': ['TST'],
                'Indicator Name': ['test'],
                'Indicator Code': ['test'],
                '2001': [1],
                '2002': [1],
                '2003': [1],
                '2004': [1],
                '2005': [1],
                '2006': [1],
                '2007': [1]}
        df2 = pd.DataFrame(data)
        data = {'Year': [2003, 2004, 2005, 2006, 2007, 2008],
                'Country': ['TEST1','TEST2','TEST3','TEST4', 'TEST5', 'TEST6'],
                'Total': [1, 2, 3, 4, 5, 6],
                'Solid Fuel': [1, 2, 3, 4, 5, 6],
                'Liquid Fuel': [1, 2, 3, 4, 5, 6],
                'Gas Fuel': [1, 2, 3, 4, 5, 6],
                'Cement': [1, 2, 3, 4, 5, 6],
                'Gas Flaring': [1, 2, 3, 4, 5, 6],
                'Per Capita': [1, 2, 3, 4, 5, 6],
                'Bunker fuels(Not in Total)': [1, 2, 3, 4, 5, 6]}
        df3 = pd.DataFrame(data)
        years_result = src.library.get_years_array(df1, df2, df3)

        self.assertEqual(years_result, list(range(2003, 2007)))


if __name__ == '__main__':
    unittest.main()
