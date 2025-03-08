import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Define a function to process data in chunks
def process_chunk(chunk):
    # Filter necessary columns
    chunk = chunk[['meter_id', 'location', 'consumption']]
    
    # Simulate geocoding (Replace this with actual lat/lon data)
    location_coords = {
        "North": (40.7128, -74.0060),
        "South": (34.0522, -118.2437),
        "East": (37.7749, -122.4194),
        "West": (41.8781, -87.6298)
    }
    
    chunk['latitude'] = chunk['location'].map(lambda x: location_coords.get(x, (None, None))[0] if x in location_coords else None)
    chunk['longitude'] = chunk['location'].map(lambda x: location_coords.get(x, (None, None))[1] if x in location_coords else None)
    
    return chunk.dropna()

# Read the large file in chunks with error handling
chunksize = 50000  # Adjust based on memory
gdf_list = []

try:
    for chunk in pd.read_csv(r"C:\Users\user\Desktop\Dr. Maurice\My_Ami.csv", chunksize=chunksize):
        processed_chunk = process_chunk(chunk)
        gdf_list.append(processed_chunk)
except FileNotFoundError:
    print("Error: The specified file was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

# Convert to GeoDataFrame
gdf = pd.concat(gdf_list, ignore_index=True)
gdf = gpd.GeoDataFrame(gdf, geometry=gdf.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1))

# Save to file to avoid reprocessing
gdf.to_file("processed_data.geojson", driver="GeoJSON")

# Create Map
map_center = [gdf['latitude'].mean(), gdf['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=6)

# Add points to the map
for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Save map to HTML
m.save("ami_meter_map.html")
print("Map saved as 'ami_meter_map.html'")
