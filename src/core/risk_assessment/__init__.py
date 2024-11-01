# src/core/risk_assessment/__init__.py

import logging

from .risk_analyzer import RiskAnalyzer
from .anomaly_detection import AnomalyDetector

__all__ = ['RiskAnalyzer', 'AnomalyDetector']

# Set up logging for the risk assessment module
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("risk_assessment.log"),
        logging.StreamHandler()
    ]
)

# Module version
__version__ = "1.0.0"

def initialize_risk_assessment():
    """Initialize the risk assessment module."""
    logging.info("Initializing the Risk Assessment module.")
    risk_analyzer = RiskAnalyzer()
    anomaly_detector = AnomalyDetector()
    logging.info("Risk Assessment module initialized successfully.")
    return risk_analyzer, anomaly_detector

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        logging.info("Data loaded successfully from %s", file_path)
        return data
    except Exception as e:
        logging.error("Error loading data from %s: %s", file_path, str(e))
        raise

def preprocess_data(data, target_column):
    """Preprocess data for analysis."""
    try:
        features = data.drop(columns=[target_column])
        target = data[target_column]
        logging.info("Data preprocessed successfully.")
        return features, target
    except KeyError as e:
        logging.error("Error in preprocessing data: %s", str(e))
        raise

def save_model(model, file_path):
    """Save the trained model to a file."""
    import joblib
    try:
        joblib.dump(model, file_path)
        logging.info("Model saved successfully to %s", file_path)
    except Exception as e:
        logging.error("Error saving model to %s: %s", file_path, str(e))
        raise

def load_model(file_path):
    """Load a trained model from a file."""
    import joblib
    try:
        model = joblib.load(file_path)
        logging.info("Model loaded successfully from %s", file_path)
        return model
    except Exception as e:
        logging.error("Error loading model from %s: %s", file_path, str(e))
        raise
