import sys

import geopandas as gpd
import pyogrio

# print(pyogrio.list_drivers())

infile = sys.argv[1]
outfile = sys.argv[2]
print(infile, outfile)

df = pyogrio.read_dataframe(infile)
print(df.head())
# pyogrio.write_dataframe(df, outfile, driver="FlatGeobuf")
