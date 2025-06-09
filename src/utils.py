
import h3
import requests
from tqdm import tqdm
import os
import logging
from shapely.geometry import Polygon

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- H3 Utilities ---
def geo_to_h3_safe(lat, lon, resolution):
    """Safely convert lat/lon to H3, handling potential errors."""
    try:
        if pd.isna(lat) or pd.isna(lon):
            return None
        return h3.geo_to_h3(lat, lon, resolution)
    except Exception as e: # Catches H3 CellInputError for invalid lat/lon, TypeError if lat/lon aren't float
        # logger.warning(f"H3 conversion error for lat={lat}, lon={lon}: {e}")
        return None

def get_h3_boundary_geojson(h3_index):
    """Get GeoJSON boundary for an H3 cell."""
    try:
        boundary = h3.h3_to_geo_boundary(h3_index, geo_json=True)
        # Folium Choropleth needs feature.properties.id to match key_on
        return {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [boundary]}, "properties": {"id": h3_index}}
    except Exception as e:
        logger.warning(f"Error getting H3 boundary for {h3_index}: {e}")
        return None

def get_h3_centroid(h3_index):
    """Get centroid (lat, lon) of an H3 cell."""
    try:
        lat, lon = h3.h3_to_geo(h3_index)
        return lat, lon
    except Exception as e:
        logger.warning(f"Error getting H3 centroid for {h3_index}: {e}")
        return None, None

def h3_to_polygon(h3_index):
    """Convert H3 index to a Shapely Polygon."""
    try:
        boundary = h3.h3_to_geo_boundary(h3_index, geo_json=False) # Returns list of (lat, lon) tuples
        # Shapely expects (lon, lat)
        return Polygon([(lon, lat) for lat, lon in boundary])
    except Exception as e:
        logger.warning(f"Error converting H3 {h3_index} to Polygon: {e}")
        return None


# --- File Download Utility ---
def download_file(url, filename, data_dir):
    """Helper to download file if not exists."""
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        logger.info(f"Downloading {filename} to {data_dir}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in tqdm(response.iter_content(chunk_size=8192), desc=f"Downloading {filename}"):
                    f.write(chunk)
            logger.info(f"Download complete: {filepath}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {filename}: {e}")
            return None
    else:
        logger.info(f"{filename} already exists in {data_dir}.")
    return filepath

# --- Pandas is imported where needed in other modules ---
import pandas as pd # Add here for geo_to_h3_safe if it uses pd.isna