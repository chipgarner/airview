import gpxpy
import pandas
import geopandas
import numpy as np
import json


class FilesReader:
    def __init__(self):
        pass

    def read_gpx(self, gpx_file_path):
        gpx_file = open(gpx_file_path, 'r')
        gpx = gpxpy.parse(gpx_file, version="1.1")

        trk = gpxpy.gpx.GPXTrackPoint()
        return gpx

    def gpx_to_dataframe(self, gpx_data):
        # Convert to a dataframe one point at a time.
        points = []
        for segment in gpx_data.tracks[0].segments:
            for p in segment.points:
                points.append({
                    'time': np.datetime64(p.time),  # Make type compatible with air data file for merge
                    'latitude': p.latitude,
                    'longitude': p.longitude,
                    'elevation': p.elevation,
                })
        gps_data = pandas.DataFrame.from_records(points)

        return gps_data

    def read_gpx_geopandas(self, gpx_file_path):
        return geopandas.read_file(gpx_file_path, driver='GPX', layer='tracks')

    def read_yourair_txt(self, yourair_txt_path):
        air_data = []
        with open(yourair_txt_path) as file:
            for line in file:
                dict_line = json.loads(line)
                dict_line['time'] = np.datetime64(dict_line['time'])  # Datframe merge likes this type
                air_data.append(dict_line)

        df = pandas.DataFrame(air_data)
        return df
