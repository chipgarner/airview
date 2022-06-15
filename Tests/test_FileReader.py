import pandas
import geopandas

import files_reader


def assert_file_data(gpx_data):
    assert len(gpx_data.tracks[0].segments[0].points) == 555

    track_point = gpx_data.tracks[0].segments[0].points[7]
    assert track_point.time.timestamp() == 1653261772.0


def test_read_garmin_pgx():
    path = "Data/run_garmin.gpx"
    fr = files_reader.FilesReader()

    gpx_data = fr.read_gpx(path)

    assert_file_data(gpx_data)


def test_read_strava_gps():
    path = "Data/run_strava.gpx"
    fr = files_reader.FilesReader()

    gpx_data = fr.read_gpx(path)

    assert_file_data(gpx_data)


def test_reads_extensions():
    path = "Data/run_garmin.gpx"
    fr = files_reader.FilesReader()

    gpx_data = fr.read_gpx(path)
    print(gpx_data)

    hr = []
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                for ext in point.extensions:
                    for ext_child in list(ext):
                        if 'hr' in ext_child.tag:
                            hr.append(int(ext_child.text))

    assert len(hr) == 555
    assert hr[551] == 111


def test_read_file_from_pi():

    path = "Data/walk_pi1.txt"
    fr = files_reader.FilesReader()
    df = fr.read_yourair_txt(path)

    assert type(df) == pandas.core.frame.DataFrame
    assert df.size == 1908
    assert df.columns.values[0] == 'time'
    assert df.columns.values[1] == '1.0 ug/m3'
    assert df.columns.values[11] == 'PM 2.5 EPA'
    print(df.values[20])
    assert df.values[20][0] == pandas.Timestamp('2022-06-14 16:14:29')


def test_combo():
    path = "Data/walk_pi1.txt"
    fr = files_reader.FilesReader()
    air_data = fr.read_yourair_txt(path)
    print(air_data)

    path = "Data/walk_garmin.gpx"
    gpx_data = fr.read_gpx(path)

    gps_data = fr.gpx_to_dataframe(gpx_data)
    print(gps_data)

    df = pandas.merge_asof(gps_data, air_data, on='time')
    print(df)

    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))

    gdf['time'] = gdf['time'].astype(str)  # Convert times back to string for map

    map = gdf.explore()
    map.save('map.html')
    import webbrowser
    webbrowser.open('map.html')
