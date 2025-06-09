import os
from pathlib import Path

# --- Project Root ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Data Paths ---
# --- Data Paths ---
DATA_DIR = PROJECT_ROOT / "data"
RAW_TAXI_DATA_FILE = DATA_DIR / "yellow_tripdata_2015-01.csv" # Download this manually
BOROUGHS_GEOJSON_URL = "https://data.cityofnewyork.us/api/geospatial/tqmj-j8zm?method=export&format=GeoJSON"
BOROUGHS_FILE_NAME = "borough.geo.json"
BOROUGHS_FILE_PATH = DATA_DIR / BOROUGHS_FILE_NAME

# --- Processed Data Paths ---
PREPROCESSED_DATA_DIR = DATA_DIR / "processed"
PREPROCESSED_TAXI_DATA_FILE = PREPROCESSED_DATA_DIR / "preprocessed_taxi_data.parquet"
FEATURE_ENGINEERED_DATA_FILE = PREPROCESSED_DATA_DIR / "feature_engineered_demand.parquet"
CLUSTERED_DATA_FILE = PREPROCESSED_DATA_DIR / "clustered_demand.parquet"

# --- Model Paths ---
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_FILE = MODEL_DIR / "lgbm_demand_forecaster.joblib" # Using joblib for scikit-learn compatible models

# --- Report Paths ---
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MAPS_DIR = REPORTS_DIR / "maps"

# --- Feature Engineering & Modeling Params ---
BOROUGH_TO_FILTER = 'Manhattan'
H3_RESOLUTION = 9 # Finer granularity, ~0.278 km² area
N_CLUSTERS_HOTSPOTS = 10
TARGET_COLUMN = 'demand'
TEST_DAYS = 3 # Number of days for the test set

# Lag features (hours)
LAG_FEATURES_HOURS = [1, 2, 3, 6, 12, 24, 24*2, 24*7] # 1h to 1 week

# Moving average windows (hours)
MA_WINDOWS_HOURS = [3, 6, 12, 24, 24*7]

# Ensure directories exist
PREPROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
MAPS_DIR.mkdir(parents=True, exist_ok=True)

# --- LightGBM Parameters (example, can be tuned) ---
LGBM_PARAMS = {
    'objective': 'regression_l1', # MAE
    'metric': 'mae',
    'n_estimators': 1000,
    'learning_rate': 0.05,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 1,
    'verbose': -1,
    'n_jobs': -1,
    'seed': 42,
    'boosting_type': 'gbdt',
    # 'force_col_wise': True # Can sometimes speed up training with many features
}
LGBM_EARLY_STOPPING_ROUNDS = 100

# --- Columns ---
# Define common column names to avoid typos
PICKUP_DATETIME_COL = 'tpep_pickup_datetime'
DROPOFF_DATETIME_COL = 'tpep_dropoff_datetime'
PICKUP_LAT_COL = 'pickup_latitude'
PICKUP_LON_COL = 'pickup_longitude'
PICKUP_H3_COL = 'pickup_h3_zone'
PICKUP_HOUR_TS_COL = 'pickup_hour_timestamp'

# Features that will be used for training (base set, more can be added)
BASE_FEATURE_COLS = [
    'hour_of_day', 'day_of_week', 'day_of_month', 'month', 'year', 'is_weekend',
    'quarter', 'week_of_year'
]
# Categorical features for LightGBM (pickup_h3_zone will be added dynamically)
CATEGORICAL_FEATURES = [
    'pickup_h3_zone', 'hour_of_day', 'day_of_week', 'month', 'year', 'is_weekend', 'demand_cluster'
]