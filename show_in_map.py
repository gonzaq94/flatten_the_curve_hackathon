import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import urllib3
import json
import numpy as np
from write2sheet import *

# we create the dictionary from postcodes to gps positions

url = 'https://data.nsw.gov.au/data/api/3/action/datastore_search_sql?sql=SELECT * from "21304414-1ff1-4243-a5d2-f52778048b29"'

df = pd.read_csv('Australian_Post_Codes_Lat_Lon.csv')
df = pd.DataFrame(df[['postcode', 'lat', 'lon']])
df = df.dropna()

post2lat = pd.Series(df.lat.values, index=df.postcode.values).to_dict()
post2lon = pd.Series(df.lon.values, index=df.postcode.values).to_dict()

# read data from government's page

http = urllib3.PoolManager()
r = http.request('GET', url)
print('Status code: ', r.status)

data_dic = json.loads(r.data.decode('utf-8'))
data = data_dic['result']['records']

df = pd.DataFrame(data)
df = pd.DataFrame(df['postcode'])
df['cases'] = df.postcode.map(df.postcode.value_counts())
df = df.drop_duplicates()
df = df.dropna()
cases = df['cases']

postcodes = np.array(df['postcode']).astype('uint16')

latitudes = np.array([post2lat.get(pc, np.nan) for pc in postcodes])
longitudes = np.array([post2lon.get(pc, np.nan) for pc in postcodes])

nan_array = np.isnan(latitudes)
not_nan_array = ~ nan_array

geometry = [Point(xy) for xy in zip(longitudes, latitudes)]
crs = {'init': 'epsg:4326'}
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
geo_df = geo_df.dropna()

# we load Australia's map

street_map = gpd.read_file('AUS_rds/AUS_roads.shp')

fig, ax = plt.subplots(figsize=(15, 15))
street_map.plot(ax = ax)
geo_df.plot(ax = ax, color='red', markersize=10*geo_df['cases'])
plt.ylim([-36, -32])
plt.xlim([147, 152])
plt.grid()
plt.axis('off')
plt.savefig('sidney1.png')
plt.show()

# finally, we write data to  google sheet

df = pd.DataFrame({'long': longitudes,'lat': latitudes,'cases': cases})
df = df.dropna()

SAMPLE_SPREADSHEET_ID_input = '1FoFTYQA8niwqQz7OpqY-M2nfT4YEnp37ZxhpW_tDWHs'
SAMPLE_RANGE_NAME = 'A1:AA1000'

Create_Service('credentials.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])
Export_Data_To_Sheets(df, SAMPLE_SPREADSHEET_ID_input, SAMPLE_RANGE_NAME)