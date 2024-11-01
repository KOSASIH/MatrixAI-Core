# reputation/reputation_manager.py

import logging
import pandas as pd
from .scoring_algorithm import ScoringAlgorithm

class ReputationManager:
    """Class for managing reputation scores."""

    def __init__(self, scoring_algorithm: ScoringAlgorithm):
        self.scoring_algorithm = scoring_algorithm
        self.scores = pd.DataFrame(columns=['entity', 'score'])
        logging.info("ReputationManager initialized with %s.", self.scoring_algorithm.__class__.__name__)

    def add_entity(self, entity: str, data: dict):
        """Add an entity and its associated data for scoring."""
        try:
            score = self.scoring_algorithm.calculate_score(data)
            self.scores = self.scores.append({'entity': entity, 'score': score}, ignore_index=True)
            logging.info("Entity %s added with score: %.2f", entity, score)
        except Exception as e:
            logging.error("Error adding entity %s: %s", entity, str(e))

    def add_entities(self, entities: dict):
        """Add multiple entities and their associated data for scoring."""
        for entity, data in entities.items():
            self.add_entity(entity, data)

    def get_score(self, entity: str):
        """Get the reputation score for a specific entity."""
        score_row = self.scores[self.scores['entity'] == entity]
        if not score_row.empty:
            score = score_row['score'].values[0]
            logging.info("Retrieved score for %s: %.2f", entity, score)
            return score
        else:
            logging.warning("Entity %s not found.", entity)
            return None

    def get_all_scores(self):
        """Get all reputation scores."""
        logging.info("Retrieved all scores.")
        return self.scores

    def update_entity_score(self, entity: str, new_data: dict):
        """Update the score for an existing entity."""
        if entity in self.scores['entity'].values:
            try:
                new_score = self.scoring_algorithm.calculate_score(new_data)
                self.scores.loc[self.scores['entity'] == entity, 'score'] = new_score
                logging.info("Updated score for %s: %.2f", entity, new_score)
            except Exception as e:
                logging.error("Error updating score for %s: %s", entity, str(e))
        else:
            logging.warning("Entity %s not found for update.", entity)

    def remove_entity(self, entity: str):
        """Remove an entity from the reputation scores."""
        if entity in self.scores['entity'].values:
            self.scores = self.scores[self.scores['entity'] != entity]
            logging.info("Entity %s removed from scores.", entity)
        else:
            logging.warning("Entity %s not found for removal.", entity)

    def batch_update_scores(self, updates: dict):
        """Batch update scores for multiple entities."""
        for entity, new_data in updates.items():
            self.update_entity_score(entity, new_data)

    def save_scores(self, file_path: str):
        """Save the current scores to a CSV file."""
        try:
            self.scores.to_csv(file_path, index=False)
            logging.info("Scores saved to %s.", file_path)
        except Exception as e:
            logging.error("Error saving scores to %s: %s", file_path, str(e))

    def load_scores(self, file_path: str):
        """Load scores from a CSV file."""
        try:
            loaded_scores = pd.read_csv(file_path)
            if 'entity' in loaded_scores.columns and 'score' in loaded_scores.columns:
                self.scores = loaded_scores
                logging.info("Scores loaded from %s.", file_path)
            else:
                logging.error("Invalid format in %s. Required columns: 'entity', 'score'.", file_path)
        except Exception as e:
            logging.error("Error loading scores from %s: %s", file_path, str(e))
