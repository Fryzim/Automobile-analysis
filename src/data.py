"""Loading and cleaning the automobile dataset."""
import pandas as pd

QUANTITATIVE_VARS = [
    'miles_per_gallon', 'cylinders', 'displacement',
    'horsepower', 'weight_lbs', 'acceleration', 'model_year',
]

ORIGIN_MAP = {1: 'USA', 2: 'Europe', 3: 'Japan'}

CAFE_THRESHOLD_MPG = 24


def load_data(path="automobiles.csv"):
    return pd.read_csv(path)


def clean_data(df):
    """Drops missing rows and adds two derived columns:
    - origin_name: human-readable version of origin_country
    - meets_cafe: whether the car meets the 24 mpg CAFE threshold
    """
    df_clean = df.dropna().copy()
    df_clean['origin_name'] = df_clean['origin_country'].map(ORIGIN_MAP)
    df_clean['meets_cafe'] = df_clean['miles_per_gallon'] >= CAFE_THRESHOLD_MPG
    return df_clean
