import os, sys
import time
from src.configuration.configuration import Configuration
from src.component.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataCleaningArtifact, DataManipulationArtifact
from src.component.data_validation import DataValidation
from src.component.data_cleaning import DataCleaning
from src.component.data_manipulation import DataManipulation
from src.component.model_generator import ModelGenerator

class Pipeline:
    
    def __init__(self, movie_name, movie_genre, config : Configuration = Configuration()) -> None:
        try:
            self.config = config
            self.movie_name = movie_name
            self.movie_genre = movie_genre
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e

    def start_data_cleaning(self, data_ingestion_artifact: DataIngestionArtifact) -> DataCleaningArtifact:
        try:
            data_cleaning = DataCleaning(data_cleaning_config=self.config.get_data_cleaning_config(),
                                         data_ingestion_artifact=data_ingestion_artifact)
            data_cleaning_artifact = data_cleaning.initiate_data_cleaning()
            return data_cleaning_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_validation(self, data_cleaning_artifact: DataCleaningArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_cleaning_artifact=data_cleaning_artifact
                                             )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_manipulation(self, data_validation_artifact: DataValidationArtifact) -> DataManipulationArtifact:
        try:
            data_manipulation = DataManipulation(data_manipulation_config=self.config.get_data_manipulation_config(),
                                                 data_validation_artifact=data_validation_artifact)
            return data_manipulation.initiate_data_manipulation()
        except Exception as e:
            raise Exception(e, sys) from e
    
    def start_model_generation(self, data_manipulation_artifact: DataManipulationArtifact):
        try:
            model_trainer =  ModelGenerator(movie_name=self.movie_name, movie_genre=self.movie_genre,model_generation_config=self.config.get_model_generator_config(),
                                            data_manipulation_artifact=data_manipulation_artifact)
            return model_trainer.initiate_model_training()
        except Exception as e:
            raise Exception(e, sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_cleaning_artifact = self.start_data_cleaning(data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = self.start_data_validation(data_cleaning_artifact=data_cleaning_artifact)
            data_manipulation_artifact = self.start_data_manipulation(data_validation_artifact=data_validation_artifact)
            model_generation_artifact = self.start_model_generation(data_manipulation_artifact=data_manipulation_artifact)
            return model_generation_artifact
        except Exception as e:
            raise Exception(e, sys) from e