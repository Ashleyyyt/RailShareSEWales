import pandas as pd
import warnings
import geopandas as gpd
import googlemaps
from datetime import datetime
warnings.filterwarnings("ignore")

#Load station shapefile
station_catchment_gpd = gpd.read_file("Data/Station Catchment & Frequency/800m Station Catchment Shapefiles/0_All SE Wales Stations.shp")
station_catchment_gpd = station_catchment_gpd.to_crs('epsg:4326')
samples = station_catchment_gpd.sample_points(30)

sample_coords = []
for area_sample in samples:
    placeholder = []
    for sample in area_sample.geoms:
        placeholder.append((sample.x, sample.y))
    sample_coords.append(placeholder)
#lat = centroids.y
#lon = centroids.x

gmaps = googlemaps.Client(key='AIzaSyBQIY1exi4C89RtHCExkodFMNYoI1TRFRY')

time = datetime(2023, 7, 17, 8, 30)
all_samples = []
for sample_area in sample_coords:
    area_list = []
    for sample in sample_area:
        point = str(sample[1]) + "," + str(sample[0])
        dest = "51.47614863414888, -3.179411924030065"
        dirs  = gmaps.directions(point, dest, mode="driving", departure_time=time)
        duration = dirs[0]["legs"][0]["duration"]["value"] #seconds
        area_list.append(duration)
    all_samples.append(area_list)

#Get Station Name and Code
splits = station_catchment_gpd["MERGE_SRC"].str.split("_")
cols = []
for row in splits:
    cols.append(row[1])

#Save as csv
df = pd.DataFrame(all_samples).transpose()
df.columns = cols
df.to_csv
df.to_csv("Data/Journey Time & Rail Share/GoogleMapsPeakWeekdayJourneyTimes.csv")


