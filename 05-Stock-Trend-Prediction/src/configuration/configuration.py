import os, sys
import logging

from datetime import datetime

from src.constants import *
from src.utils import *
from src.entity.config_entity import DataIngestionConfig, DataPreprocessingConfig, DataProcessingConfig, ModelTrainingConfig, ModelPredictionConfig, TrainingPipelineConfig

class Configuration:
    
    def __init__(self, config_file_path:str=CONFIG_FILE_PATH) -> None:
        try:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            self.logger.info(f"Fetching the configuration Data from {config_file_path}")
            self.config_file_path = config_file_path
            self.config_info = read_yaml_file(self.config_file_path)
            self.time_stamp = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
            self.training_pipeline_config = self.get_training_pipeline_config()
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                data_ingestion_config_info[DATA_INGESTION_ARTIFACT_DIR_KEY]
            )
            dataset_file_name = data_ingestion_config_info[DATA_INGESTION_DATASET_FILE_NAME_KEY]
            dataset_file_path = os.path.join(data_ingestion_artifact_dir, dataset_file_name)
            data_ingestion_config = DataIngestionConfig(
                ingested_data_file_path=dataset_file_path,
            )
            return data_ingestion_config
        
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_preprocessing_config_info = self.config_info[DATA_PREPROCESSING_CONFIG_KEY]
            data_preprocessing_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                data_preprocessing_config_info[DATA_PREPROCESSING_ARTIFACT_DIR_KEY]
            )
            preprocessing_data_file_name = data_preprocessing_config_info[DATA_PREPROCESSING_DATASET_FILE_NAME_KEY]
            preprocessing_data_file_path = os.path.join(data_preprocessing_artifact_dir, preprocessing_data_file_name)
            data_preprocessing_config = DataPreprocessingConfig(
                preprocessing_data_file_path = preprocessing_data_file_path
            )
            return data_preprocessing_config
        
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_data_processing_config(self) -> DataProcessingConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_processing_config_info = self.config_info[DATA_PROCESSING_CONFIG_KEY]
            data_processing_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                data_processing_config_info[DATA_PROCESSING_ARTIFACT_DIR_KEY]
            )
            processing_data_file_name = data_processing_config_info[DATA_PROCESSING_DATASET_FILE_NAME_KEY]
            processing_data_file_path = os.path.join(data_processing_artifact_dir, processing_data_file_name)

            processing_moving_averages_dir_name = data_processing_config_info[DATA_PROCESSING_MOVING_AVERAGES_DIR_KEY]
            processing_moving_averages_dir_path = os.path.join(data_processing_artifact_dir, processing_moving_averages_dir_name)

            processing_fifty_moving_average_file_name = data_processing_config_info[DATA_PROCESSING_FIFTY_MOVING_AVERAGE_FILE_NAME_KEY]
            processing_fifty_moving_average_file_path = os.path.join(processing_moving_averages_dir_path, processing_fifty_moving_average_file_name)

            processing_hundred_moving_average_file_name = data_processing_config_info[DATA_PROCESSING_HUNDRED_MOVING_AVERAGE_FILE_NAME_KEY]
            processing_hundred_moving_average_file_path = os.path.join(processing_moving_averages_dir_path, processing_hundred_moving_average_file_name)

            processing_two_hundred_moving_average_file_name = data_processing_config_info[DATA_PROCESSING_TWO_HUNDRED_MOVING_AVERAGE_FILE_NAME_KEY]
            processing_two_hundred_moving_average_file_path = os.path.join(processing_moving_averages_dir_path, processing_two_hundred_moving_average_file_name)   

            processing_graphs_data_dir_name = data_processing_config_info[DATA_PROCESSING_GRAPHS_DATA_DIR_KEY]
            processing_graphs_data_dir_path = os.path.join(data_processing_artifact_dir, processing_graphs_data_dir_name)

            processing_close_price_graph_file_name = data_processing_config_info[DATA_PROCESSING_CLOSE_PRICE_GRAPH_FILE_NAME_KEY]
            processing_close_price_graph_file_path = os.path.join(processing_graphs_data_dir_path, processing_close_price_graph_file_name)

            processing_50_ma_graph_file_name = data_processing_config_info[DATA_PROCESSING_50_MA_GRAPH_FILE_NAME_KEY]
            processing_50_ma_graph_file_path = os.path.join(processing_graphs_data_dir_path, processing_50_ma_graph_file_name)

            processing_100_ma_graph_file_name = data_processing_config_info[DATA_PROCESSING_100_MA_GRAPH_FILE_NAME_KEY]
            processing_100_ma_graph_file_path = os.path.join(processing_graphs_data_dir_path, processing_100_ma_graph_file_name)

            processing_200_ma_graph_file_name = data_processing_config_info[DATA_PROCESSING_200_MA_GRAPH_FILE_NAME_KEY]
            processing_200_ma_graph_file_path = os.path.join(processing_graphs_data_dir_path, processing_200_ma_graph_file_name)

            processing_50_100_200_ma_comp_graph_file_name = data_processing_config_info[DATA_PROCESSING_50_100_200_MA_COMP_GRAPH_FILE_NAME_KEY]
            processing_50_100_200_ma_comp_graph_file_path = os.path.join(processing_graphs_data_dir_path, processing_50_100_200_ma_comp_graph_file_name)

            data_processing_config = DataProcessingConfig(
                processing_data_file_path = processing_data_file_path,
                processing_moving_averages_dir_path = processing_moving_averages_dir_path,
                processing_fifty_moving_average_file_path = processing_fifty_moving_average_file_path,
                processing_hundred_moving_average_file_path = processing_hundred_moving_average_file_path,
                processing_two_hundred_moving_average_file_path = processing_two_hundred_moving_average_file_path,
                processing_close_price_graph_file_path = processing_close_price_graph_file_path,
                processing_50_ma_graph_file_path = processing_50_ma_graph_file_path,
                processing_100_ma_graph_file_path = processing_100_ma_graph_file_path,
                processing_200_ma_graph_file_path = processing_200_ma_graph_file_path,
                processing_50_100_200_ma_comp_graph_file_path = processing_50_100_200_ma_comp_graph_file_path
            )
            return data_processing_config
        
        except Exception as e:
            raise Exception(e, sys) from e

    def get_model_training_config(self) -> ModelTrainingConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_training_config_info = self.config_info[MODEL_TRAINING_CONFIG_KEY]

            self.model_data_dir = os.path.join(
                artifact_dir,
                model_training_config_info[MODEL_DATA_DIR_KEY],
            )

            model_training_data_dir_path = os.path.join(
                self.model_data_dir,
                model_training_config_info[MODEL_TRAINING_DATA_DIR_KEY],
                self.time_stamp
            )

            model_train_data_file_name = model_training_config_info[MODEL_TRAINING_TRAIN_DATA_FILE_NAME_KEY]
            model_train_data_file_path = os.path.join(model_training_data_dir_path, model_train_data_file_name)

            model_test_data_file_name = model_training_config_info[MODEL_TRAINING_TEST_DATA_FILE_NAME_KEY]
            model_test_data_file_path = os.path.join(model_training_data_dir_path, model_test_data_file_name)

            model_file_name = model_training_config_info[MODEL_TRAINING_MODEL_FILE_NAME_KEY]
            model_file_path = os.path.join(
                self.model_data_dir,
                model_training_config_info[MODEL_TRAINING_DATA_DIR_KEY],
                model_file_name
            )

            model_training_config = ModelTrainingConfig(
                model_training_data_dir_path = model_training_data_dir_path,
                model_train_data_file_path=model_train_data_file_path,
                model_test_data_file_path=model_test_data_file_path,
                model_file_path=model_file_path
            )
            return model_training_config

        except Exception as e:
            raise Exception(e, sys) from e
    
    def get_model_prediction_config(self) -> ModelPredictionConfig:
        try:
            model_prediction_config_info = self.config_info[MODEL_PREDICTION_CONFIG_KEY]
            model_prediction_data_dir_name = model_prediction_config_info[MODEL_PREDICTION_DATA_DIR_KEY]

            model_prediction_data_dir_path = os.path.join(
                self.model_data_dir,
                model_prediction_data_dir_name,
                self.time_stamp
            )

            model_prediction_graphs_data_dir_name = model_prediction_config_info[MODEL_PREDICTION_GRAPHS_DATA_DIR__NAME_KEY]
            model_prediction_graphs_data_dir_path = os.path.join(model_prediction_data_dir_path, model_prediction_graphs_data_dir_name)

            model_prediction_predicted_graph_file_name = model_prediction_config_info[MODEL_PREDICTION_PREDICTED_GRAPH_FILE_NAME_KEY]
            model_prediction_predicted_graph_file_path = os.path.join(model_prediction_graphs_data_dir_path, model_prediction_predicted_graph_file_name)

            model_prediction_config = ModelPredictionConfig(
                model_prediction_predicted_graph_file_path = model_prediction_predicted_graph_file_path
            )
            return model_prediction_config
        
        except Exception as e:
            raise Exception(e, sys) from e 
              
    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR , DATA_DIR, training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            return training_pipeline_config
        except Exception as e:
            raise Exception(e, sys) from e

