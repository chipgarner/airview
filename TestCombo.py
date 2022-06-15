#
# Combines gps data from Garmin or Strava and combines it with yourair data using timestamps
# Maps the result on an interactive map that can be copied to a web page.

import pandas
import geopandas
import webbrowser
import files_reader

path = "Tests/Data/walk_pi1.txt"
fr = files_reader.FilesReader()
air_data = fr.read_yourair_txt(path)
print(air_data)

path = "Tests/Data/walk_garmin.gpx"
gpx_data = fr.read_gpx(path)

gps_data = fr.gpx_to_dataframe(gpx_data)
print(gps_data)

df = pandas.merge_asof(gps_data, air_data, on='time')
print(df)

gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude), crs='EPSG:4326')

gdf['time'] = gdf['time'].astype(str)  # Convert times back to string for map

map = gdf.explore(column='PM 2.5 EPA', cmap='summer')
map.save('map2.html')

webbrowser.open('map2.html')

print(gdf)
print(gdf.to_dict())
print(gdf.to_dict()['geometry'])
print(gdf.to_dict()['geometry'][12])
