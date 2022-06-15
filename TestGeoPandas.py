import geopandas
import webbrowser
import matplotlib.pyplot as plt

gdf = geopandas.read_file("Tests/Data/walk_strava.gpx", driver='GPX', layer='tracks')
map = gdf.explore()
map.save('map.html')
webbrowser.open('map.html')

print(gdf)
print(gdf.to_dict()['geometry'][0])



# gdf.plot()
# plt.show()