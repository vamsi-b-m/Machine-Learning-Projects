import os, sys
import logging

from src.configuration.configuration import Configuration
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import Data_Preprocessing
from src.components.data_processing import DataProcessing
from src.components.model_training import ModelTraining
from src.components.model_prediction import ModelPrediction
from src.entity.artifact_entity import DataIngestionArtifact, DataPreprocessingArtifact, DataProcessingArtifact, ModelTrainingArtifact, ModelPredictionArtifact

class Pipeline:

    def __init__(self, config : Configuration = Configuration()) -> None:
        try:
            self.config = config
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.logger.info("Started Data Ingestion")
            data_ingestion = DataIngestion(
                stock_symbol=self.stock_symbol,
                data_ingestion_config=self.config.get_data_ingestion_config()
                )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            self.logger.info(f"Completed Data Ingestion\nData Ingestion Artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e
    
    def start_data_preprocessing(self, data_ingestion_artifact : DataIngestionArtifact) -> DataPreprocessingArtifact:
        try:
            self.logger.info("Started Data Preprocessing")
            data_preprocessing = Data_Preprocessing(
                data_preprocessing_config=self.config.get_data_preprocessing_config(),
                data_ingestion_artifact=data_ingestion_artifact
            )
            data_preprocessing_artifact = data_preprocessing.initiate_data_preprocessing()
            self.logger.info(f"Completed Data Preprocessing\nData Preprocessing Artifact : {data_preprocessing_artifact}")
            return data_preprocessing_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_data_processing(self, data_ingestion_artifact : DataIngestionArtifact, data_preprocessing_artifact:DataPreprocessingArtifact) -> DataProcessingArtifact:
        try:
            self.logger.info("Started Data Processing")
            data_processing = DataProcessing(
                data_processing_config=self.config.get_data_processing_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_preprocessing_artifact=data_preprocessing_artifact
            )
            data_processing_artifact = data_processing.initiate_data_processing()
            self.logger.info(f"Completed Data Processing\nData Processing Artifact : {data_processing_artifact}")
            return data_processing_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def start_model_training(self, data_processing_artifact:DataPreprocessingArtifact) -> ModelTrainingArtifact:
        try:
            self.logger.info("Started Model Training")
            model_training = ModelTraining(
                model_training_config=self.config.get_model_training_config(),
                data_processing_artifact=data_processing_artifact
            )
            model_training_artifact = model_training.initiate_model_training()
            self.logger.info(f"Completed Model Training\nModel Training Artifact : {model_training_artifact}")
            return model_training_artifact
        except Exception as e:
            raise Exception(e, sys) from e
    
    def start_model_prediction(self, data_ingestion_artifact: DataIngestionArtifact, model_training_artifact: ModelTrainingArtifact) -> ModelPredictionArtifact:
        try:
            self.logger.info("Started Model Prediction")
            model_prediction = ModelPrediction(
                model_prediction_config=self.config.get_model_prediction_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                model_training_artifact=model_training_artifact
            )
            model_prediction_artifact = model_prediction.initiate_model_prediction()
            self.logger.info(f"Completed Model Prediction\nModel Prediction Artifact : {model_prediction_artifact}")
            return model_prediction_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def run_pipeline(self, stock_symbol) -> None:
        try:
            self.stock_symbol = stock_symbol
            data_ingestion_artifact = self.start_data_ingestion()
            data_preprocessing_artifact = self.start_data_preprocessing(data_ingestion_artifact=data_ingestion_artifact)
            data_processing_artifact = self.start_data_processing(data_ingestion_artifact=data_ingestion_artifact, data_preprocessing_artifact=data_preprocessing_artifact)
            model_training_artifact = self.start_model_training(data_processing_artifact=data_processing_artifact)
            model_prediction_artifact = self.start_model_prediction(data_ingestion_artifact=data_ingestion_artifact, model_training_artifact=model_training_artifact)
            graph_1 = data_processing_artifact.processing_close_price_graph_file_path
            graph_2 = data_processing_artifact.processing_200_ma_graph_file_path
            graph_3 = model_prediction_artifact.model_prediction_predicted_graph_file_path
            return graph_1, graph_2, graph_3
        except Exception as e:
            raise Exception(e, sys) from e