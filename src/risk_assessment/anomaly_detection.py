# src/risk_assessment/anomaly_detection.py

import numpy as np
import pandas as pd
import logging
from sklearn.ensemble import IsolationForest, LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

class AnomalyDetector:
    """Class for detecting anomalies in data using various algorithms."""

    def __init__(self, model_type='IsolationForest'):
        self.model_type = model_type
        self.model = self._initialize_model()
        self.scaler = StandardScaler()
        logging.info(f"AnomalyDetector initialized with {self.model_type}.")

    def _initialize_model(self):
        """Initialize the model based on the specified type."""
        if self.model_type == 'IsolationForest':
            return IsolationForest(contamination=0.05, random_state=42)
        elif self.model_type == 'LocalOutlierFactor':
            return LocalOutlierFactor(n_neighbors=20)
        else:
            logging.error("Unsupported model type: %s", self.model_type)
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def fit(self, data):
        """Fit the anomaly detection model to the data."""
        scaled_data = self.scaler.fit_transform(data)
        self.model.fit(scaled_data)
        logging.info("Anomaly detection model fitted to data.")

    def detect_anomalies(self, new_data):
        """Detect anomalies in new data."""
        scaled_data = self.scaler.transform(new_data)
        if self.model_type == 'IsolationForest':
            predictions = self.model.predict(scaled_data)
            anomalies = np.where(predictions == -1, True, False)
        elif self.model_type == 'LocalOutlierFactor':
            predictions = self.model.fit_predict(scaled_data)
            anomalies = np.where(predictions == -1, True, False)
        else:
            logging.error("Unsupported model type: %s", self.model_type)
            raise ValueError(f"Unsupported model type: {self.model_type}")

        logging.info("Anomalies detected in new data.")
        return anomalies

    def get_anomaly_scores(self, new_data):
        """Get anomaly scores for new data."""
        scaled_data = self.scaler.transform(new_data)
        if self.model_type == 'IsolationForest':
            scores = self.model.decision_function(scaled_data)
        elif self.model_type == 'LocalOutlierFactor':
            scores = -self.model.negative_outlier_factor_
        else:
            logging.error("Unsupported model type: %s", self.model_type)
            raise ValueError(f"Unsupported model type: {self.model_type}")

        logging.info("Anomaly scores calculated.")
        return scores

    def evaluate_model(self, true_labels, predictions):
        """Evaluate the anomaly detection model."""
        report = classification_report(true_labels, predictions)
        cm = confusion_matrix(true_labels, predictions)

        logging.info("Model evaluation completed.")
        logging.info("Classification Report:\n%s", report)
        logging.info("Confusion Matrix:\n%s", cm)

    def hyperparameter_tuning(self, data, contamination_range):
        """Perform hyperparameter tuning for Isolation Forest."""
        if self.model_type != 'IsolationForest':
            logging.error("Hyperparameter tuning is only supported for Isolation Forest.")
            raise ValueError("Hyperparameter tuning is only supported for Isolation Forest.")

        best_contamination = None
        best_score = -np.inf

        for contamination in contamination_range:
            model = IsolationForest(contamination=contamination, random_state=42)
            scaled_data = self.scaler.fit_transform(data)
            model.fit(scaled_data)

            # Evaluate the model using cross-validation
            predictions = model.predict(scaled_data)
            score = np.mean(predictions == -1)  # Proportion of detected anomalies

            if score > best_score:
                best_score = score
                best_contamination = contamination

        logging.info("Hyperparameter tuning completed.")
        logging.info("Best Contamination: %.2f", best_contamination)
        logging.info("Best Score: %.2f", best_score)

        # Update the model with the best contamination
        self.model = IsolationForest(contamination=best_contamination, random_state=42)
        self.fit(data)  # Re-fit the model with the best contamination
