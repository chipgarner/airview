import gpxpy
import gpxpy.gpx

with open("Tests/Data/Lunch_Ride_Modified.gpx") as gpx_file:
    gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            for ext in point.extensions:
                print(ext.tag)
                for extchild in list(ext):
                    print('{0} -> {1}'.format(extchild.tag, extchild.text))