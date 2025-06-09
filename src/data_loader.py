import os
import pandas as pd
import geopandas as gpd
from src.config import RAW_TAXI_DATA_FILE, BOROUGHS_FILE_PATH, DATA_DIR
from src.utils import logger

def load_raw_taxi_data() -> pd.DataFrame:
    """Loads the raw taxi trip data from the Parquet file."""
    if not RAW_TAXI_DATA_FILE.exists():
        logger.error(f"Raw taxi data file not found: {RAW_TAXI_DATA_FILE}")
        logger.error("Please download it from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
        logger.error(f"And place it as {RAW_TAXI_DATA_FILE.name} in the {DATA_DIR} directory.")
        raise FileNotFoundError(f"Raw taxi data file not found: {RAW_TAXI_DATA_FILE}")
    
    logger.info(f"Loading raw taxi data from {RAW_TAXI_DATA_FILE}...")
    df = pd.read_csv(RAW_TAXI_DATA_FILE)
    logger.info(f"Loaded {len(df)} trips.")
    return df

def load_borough_boundaries() -> gpd.GeoDataFrame | None:
    """
    Loads NYC borough boundaries from GeoJSON file.
    The file must be manually downloaded from:
    https://raw.githubusercontent.com/nycehs/NYC_geography/main/borough.geo.json
    """
    if not BOROUGHS_FILE_PATH.exists():
        logger.error(f"Boroughs GeoJSON file not found: {BOROUGHS_FILE_PATH}")
        logger.error("Download it manually from:")
        logger.error("https://raw.githubusercontent.com/nycehs/NYC_geography/main/borough.geo.json")
        logger.error(f"And place it in the {DATA_DIR} directory.")
        return None

    logger.info(f"Loading borough boundaries from {BOROUGHS_FILE_PATH}...")
    try:
        boroughs_gdf = gpd.read_file(BOROUGHS_FILE_PATH)
        logger.info("Borough boundaries loaded successfully.")
        return boroughs_gdf
    except Exception as e:
        logger.error(f"Error loading borough GeoJSON: {e}")
        return None

if __name__ == '__main__':
    taxi_df = load_raw_taxi_data()
    print(taxi_df.head())
    
    boroughs = load_borough_boundaries()
    if boroughs is not None:
        print(boroughs.head())
