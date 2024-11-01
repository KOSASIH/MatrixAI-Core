# src/utils/data_processing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def clean_data(df: pd.DataFrame, drop_na: bool = True) -> pd.DataFrame:
    """Clean the DataFrame by dropping or filling missing values."""
    if drop_na:
        return df.dropna()
    else:
        return df.fillna(df.mean())

def normalize_data(df: pd.DataFrame, method: str = 'minmax') -> pd.DataFrame:
    """Normalize the DataFrame using specified method."""
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Normalization method must be 'minmax' or 'standard'.")

    return pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

def split_data(df: pd.DataFrame, target_column: str, test_size: float = 0.2) -> tuple:
    """Split the DataFrame into features and target, then into training and testing sets."""
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=test_size, random_state=42)
