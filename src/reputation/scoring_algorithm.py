# reputation/scoring_algorithm.py

import numpy as np
import logging

class ScoringAlgorithm:
    """Base class for scoring algorithms."""
    def calculate_score(self, data: dict) -> float:
        """Calculate the reputation score based on input data."""
        raise NotImplementedError("Subclasses should implement this method.")

class SimpleAverageScore(ScoringAlgorithm):
    """Simple average scoring algorithm."""
    def calculate_score(self, data: dict) -> float:
        """Calculate score as the average of the values in the data dictionary."""
        if not data:
            logging.warning("No data provided for scoring.")
            return 0.0
        try:
            score = np.mean(list(data.values()))
            logging.info("Calculated Simple Average Score: %.2f", score)
            return score
        except Exception as e:
            logging.error("Error calculating Simple Average Score: %s", str(e))
            return 0.0

class WeightedScore(ScoringAlgorithm):
    """Weighted scoring algorithm."""
    def calculate_score(self, data: dict, weights: dict = None) -> float:
        """Calculate score as a weighted sum of the values in the data dictionary."""
        if weights is None:
            weights = {key: 1 for key in data.keys()}  # Default weights
        try:
            score = sum(data[key] * weights.get(key, 0) for key in data.keys())
            logging.info("Calculated Weighted Score: %.2f", score)
            return score
        except Exception as e:
            logging.error("Error calculating Weighted Score: %s", str(e))
            return 0.0

class ExponentialDecayScore(ScoringAlgorithm):
    """Exponential decay scoring algorithm."""
    def calculate_score(self, data: dict, decay_rate: float = 0.1) -> float:
        """Calculate score using an exponential decay formula."""
        if not data:
            logging.warning("No data provided for scoring.")
            return 0.0
        try:
            scores = [value * np.exp(-decay_rate * idx) for idx, value in enumerate(data.values())]
            final_score = sum(scores)
            logging.info("Calculated Exponential Decay Score: %.2f", final_score)
            return final_score
        except Exception as e:
            logging.error("Error calculating Exponential Decay Score: %s", str(e))
            return 0.0

class CustomScore(ScoringAlgorithm):
    """Custom scoring algorithm that allows for user-defined scoring logic."""
    def __init__(self, scoring_function):
        self.scoring_function = scoring_function

    def calculate_score(self, data: dict) -> float:
        """Calculate score using a custom scoring function."""
        if not callable(self.scoring_function):
            logging.error("Provided scoring function is not callable.")
            return 0.0
        try:
            score = self.scoring_function(data)
            logging.info("Calculated Custom Score: %.2f", score)
            return score
        except Exception as e:
            logging.error("Error calculating Custom Score: %s", str(e))
            return 0.0
