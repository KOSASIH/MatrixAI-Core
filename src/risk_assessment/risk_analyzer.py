# src/risk_assessment/risk_analyzer.py

import numpy as np
import pandas as pd
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

class RiskAnalyzer:
    """Class for analyzing risk using various algorithms."""

    def __init__(self, model_type='RandomForest'):
        self.model_type = model_type
        self.model = self._initialize_model()
        self.scaler = StandardScaler()
        logging.info(f"RiskAnalyzer initialized with {self.model_type}.")

    def _initialize_model(self):
        """Initialize the model based on the specified type."""
        if self.model_type == 'RandomForest':
            return RandomForestClassifier(n_estimators=100, random_state=42)
        elif self.model_type == 'GradientBoosting':
            return GradientBoostingClassifier(n_estimators=100, random_state=42)
        else:
            logging.error("Unsupported model type: %s", self.model_type)
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def train_model(self, data, target):
        """Train the risk analysis model."""
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)

        # Evaluate the model
        self.evaluate_model(X_test, y_test)

    def evaluate_model(self, X_test, y_test):
        """Evaluate the trained model."""
        X_test_scaled = self.scaler.transform(X_test)
        predictions = self.model.predict(X_test_scaled)
        report = classification_report(y_test, predictions)
        cm = confusion_matrix(y_test, predictions)

        logging.info("Model evaluation completed.")
        logging.info("Classification Report:\n%s", report)
        logging.info("Confusion Matrix:\n%s", cm)

    def predict_risk(self, new_data):
        """Predict risk for new data."""
        new_data_scaled = self.scaler.transform(new_data)
        predictions = self.model.predict(new_data_scaled)
        logging.info("Risk predictions made for new data.")
        return predictions

    def feature_importance(self, feature_names):
        """Get feature importance from the trained model."""
        importance = self.model.feature_importances_
        feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
        feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
        logging.info("Feature importance calculated.")
        return feature_importance

    def hyperparameter_tuning(self, data, target, param_grid):
        """Perform hyperparameter tuning using GridSearchCV."""
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)

        grid_search = GridSearchCV(self.model, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train_scaled, y_train)

        best_params = grid_search.best_params_
        best_score = grid_search.best_score_
        logging.info("Hyperparameter tuning completed.")
        logging.info("Best Parameters: %s", best_params)
        logging.info("Best Cross-Validation Score: %.2f", best_score)

        # Update the model with the best parameters
        self.model.set_params(**best_params)
        self.train_model(data, target)  # Re-train with the best parameters
