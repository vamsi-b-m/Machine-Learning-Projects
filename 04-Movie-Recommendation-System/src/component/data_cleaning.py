import os
import logging
import pandas as pd
from src.utils import load_data, save_data
from src.entity.artifact_entity import DataIngestionArtifact, DataCleaningArtifact
from src.entity.config_entity import DataIngestionConfig, DataCleaningConfig

class DataCleaning:
    
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_cleaning_config: DataCleaningConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_cleaning_config = data_cleaning_config
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            self.logger.exception("Error occurred during initialization", exc_info=True)
            raise

    def read_data(self):
        try:
            ingested_data_file_path = self.data_ingestion_artifact.ingested_data_file_path
            self.data = load_data(file_path=ingested_data_file_path)
            self.logger.info("Data loaded successfully from %s", ingested_data_file_path)
        except Exception as e:
            self.logger.exception("Error occurred while reading data", exc_info=True)
            raise

    def feature_selection(self):
        try:
            self.data = self.data[['names', 'overview', 'genre', 'date_x']]
            self.logger.info("Selected features successfully")
        except Exception as e:
            self.logger.exception("Error occurred during feature selection", exc_info=True)
            raise

    def handle_duplicates(self):
        try:
            self.data = self.data[~self.data.duplicated(subset=['names', 'overview', 'genre', 'date_x'], keep='first')]
            self.data=self.data.reset_index(drop=True)
            self.logger.info("Duplicates handled successfully")
        except Exception as e:
            self.logger.exception("Error occurred during handling duplicates", exc_info=True)
            raise

    def handle_null_values(self):
        try:
            null_vals = self.data.isna().sum()
            self.data.dropna(inplace=True)
            self.data=self.data.reset_index(drop=True)
            self.logger.info("Null values handled successfully")
        except Exception as e:
            self.logger.exception("Error occurred during handling null values", exc_info=True)
            raise
        
    def save_cleaned_data(self):
        try:
            cleaned_data_dir = self.data_cleaning_config.cleaned_data_dir
            os.makedirs(cleaned_data_dir, exist_ok=True)

            cleaned_data_file_path = self.data_cleaning_config.cleaned_data_file_path
            save_data(self.data, file_path=cleaned_data_file_path)
            self.logger.info("Data saved successfully to %s", cleaned_data_file_path)
            return cleaned_data_file_path
        except Exception as e:
            self.logger.exception("Error occurred during saving data", exc_info=True)
            raise

    def initiate_data_cleaning(self):
        try:
            self.logger.info("Data Cleaning Process Initiated")
            self.read_data()
            self.feature_selection()
            self.handle_duplicates()
            self.handle_null_values()
            cleaned_data_file_path = self.save_cleaned_data()
            data_cleaning_artifact = DataCleaningArtifact(
                cleaned_data_file_path=cleaned_data_file_path,
                is_cleaned=True,
                message="Data Cleaning Completed Successfully"
            )
            self.logger.info("Data Cleaning Process Completed\n")
            return data_cleaning_artifact
        except Exception as e:
            self.logger.exception("Error occurred during data cleaning process\n", exc_info=True)
            raise
