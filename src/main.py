import argparse
import library


parser = argparse.ArgumentParser(description='zaleznosci miedzy dochodami panstw, liczbami mieszkancow i emisja CO2',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('gpd', type=str)
parser.add_argument('citizens', type=str)
parser.add_argument('emission', type=str)

args = parser.parse_args()

gpd_data = library.read_data(args.gpd, 2)
cit_data = library.read_data(args.citizens, 2)
emi_data = library.read_data(args.emission, 0)


# data.columns = data.columns.astype("str")
# pandas.options.display.float_format = '{:.2f}'.format
# print(data)
