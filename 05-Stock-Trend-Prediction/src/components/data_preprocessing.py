import os, sys
import logging

import pandas as pd

from src.utils import *
from src.entity.config_entity import DataPreprocessingConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataPreprocessingArtifact

class Data_Preprocessing:

    def __init__(self, data_preprocessing_config:DataPreprocessingConfig, data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            self.data_preprocessing_config = data_preprocessing_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e
        
    def feature_selection(self):
        try:
            self.logger.info("Started Feature Selection")
            self.dataset.head()
            self.dataset['Date'] = pd.to_datetime(self.dataset['Date'])
            self.dataset = self.dataset[['Date', 'Close']]
            self.dataset = self.dataset.reset_index()
            self.logger.info(f"Selected the Features {self.dataset.columns}\n")
            self.logger.info("Completed Feature Selection")
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e
        
    def handle_null_values(self):
        try:
            self.logger.info("Started Handling Null Values")
            if self.dataset.isna().any().any():
                self.dataset = self.dataset.dropna()
                self.dataset = self.dataset.reset_index()
            else:
                pass
            self.logger.info("Completed Handling Null Values")
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e
    
    def handle_duplicate_values(self):
        try:
            self.logger.info("Started Handling Duplicates")
            if self.dataset.duplicated().any():  # Check if any duplicate rows exist
                self.dataset = self.dataset.drop_duplicates()
                self.dataset = self.dataset.reset_index()
            else:
                pass
            self.logger.info("Completed Handling Duplicates")
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e
        
    def get_preprocessed_data(self):
        try:
            ingested_data_file_path = self.data_ingestion_artifact.ingested_data_file_path
            self.dataset = read_csv_file(ingested_data_file_path)
            self.feature_selection()
            self.handle_null_values()
            self.handle_duplicate_values()
            self.preprocessed_data_file_path = self.data_preprocessing_config.preprocessing_data_file_path
            preprocessed_data_dir_path = os.path.dirname(self.preprocessed_data_file_path)
            os.makedirs(preprocessed_data_dir_path, exist_ok=True)
            self.dataset.to_csv(self.preprocessed_data_file_path, index=False)
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e
        
    def initiate_data_preprocessing(self):
        try:
            self.logger.info("Started Data Preprocessing")
            self.get_preprocessed_data()
            is_preprocessed = True
            message = "Data Preprocessing is Completed"
            data_preprocessing_artifact = DataPreprocessingArtifact(
                preprocessed_data_file_path=self.preprocessed_data_file_path,
                is_preprocessed=is_preprocessed,
                message=message
            )
            self.logger.info("Completeds Data Preprocessing")
            return data_preprocessing_artifact
            
        except Exception as e:
            self.logger.error(e)
            raise Exception(e, sys) from e

