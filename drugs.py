!pip3 install pandas
!pip3 install numpy
!pip3 install folium

import folium
## Use heatmap plugin
from folium import plugins
from folium.plugins import HeatMap

import numpy as np
import pandas as pd
import seaborn as sns

## Read data from CSV

# Read CSV into pandas
#csv_df = pd.read_csv("solr1.csv")
csv_df = pd.read_csv("foundriports.csv")

## Filter Heliports
csv_df = csv_df[~csv_df['Title'].str.contains('heliport', case=False)]


# Parse columns 'location' and 'FIM_EnName' from CSV
locations = csv_df['location']
names     = csv_df['Title']
#names     = csv_df['FIM_EnName']

## Clean the data into array of float pairs

# Remove backslashes
locations = locations.map(lambda x: x.replace("\\", ""))
names = names.map(lambda x: x.replace("`", ""))

# Examine location strings

# **NOTE: Some of this data contains text in the location column.** 
locations

# Tokenize latitude and longitude from location string
def tokenize(pos):
  return lambda locstr: locstr.split(",")[pos]

# Convert string to number and convert to numpy arrays
latitudes = locations.map(tokenize(0))
latitudes = pd.to_numeric(latitudes)
latitudes = latitudes.as_matrix()
latitudes

longitudes = locations.map(tokenize(1))
longitudes = pd.to_numeric(longitudes)
longitudes = longitudes.as_matrix()
longitudes

## Show scatterplot of locations
sns.jointplot(latitudes, longitudes) \
  .fig \
  .suptitle("Latitude vs Longitude", y=1.01)

## Creating the Map

# See https://python-visualization.github.io/folium/quickstart.html 
# for more map tutorials.
#
# A good blog post on Kaggle about Folium can also be found here:
# https://www.kaggle.com/daveianhickey/how-to-folium-for-maps-heatmaps-time-data

m = folium.Map()
# m

## Adding markers to map

# Convert to list of lat,long, name tuples
markers = list(zip(latitudes, longitudes, names))
markers = np.array(markers)
markers

# `i[:2]` slices first two elements of list which for `markers` 
# is latitude and longitude
for i in markers:
  coords = i[:2]
  title  = i[2]
  folium.Marker(location=coords, popup=title).add_to(m)
  
# m

## Adding heatmap layer
HeatMap(markers[:,:2]).add_to(m)
m

## Ports Heatmap
