import os, sys

ROOT_DIR = os.getcwd()
DATA_DIR = "data"
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
MODEL_DATA_DIR_KEY = "model_data_dir"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)

# Training pipeline related varibales
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# Data Ingestion Related Constants
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR_KEY = "data_ingestion_dir"
DATA_INGESTION_DATASET_FILE_NAME_KEY = "ingestion_dataset_file_name"
DATA_INGESTION_STOCK_SYMBOL = "stock_symbol"

# Data Preprocessing Related Constants
DATA_PREPROCESSING_CONFIG_KEY = "data_preprocessing_config"
DATA_PREPROCESSING_ARTIFACT_DIR_KEY = "data_preprocessing_dir"
DATA_PREPROCESSING_DATASET_FILE_NAME_KEY = "preprocessing_dataset_file_name"

# Data Processing Related Constants
DATA_PROCESSING_CONFIG_KEY = "data_processing_config"
DATA_PROCESSING_ARTIFACT_DIR_KEY = "data_processing_dir"
DATA_PROCESSING_DATASET_FILE_NAME_KEY = "processing_dataset_file_name"
DATA_PROCESSING_MOVING_AVERAGES_DIR_KEY = "processing_data_moving_averages_dir"
DATA_PROCESSING_FIFTY_MOVING_AVERAGE_FILE_NAME_KEY = "fifty_moving_avg_file"
DATA_PROCESSING_HUNDRED_MOVING_AVERAGE_FILE_NAME_KEY = "hundred_moving_avg_file"
DATA_PROCESSING_TWO_HUNDRED_MOVING_AVERAGE_FILE_NAME_KEY = "two_hundred_moving_avg_file"
# Graph Related Constants
DATA_PROCESSING_GRAPHS_DATA_DIR_KEY = "data_processing_graphs_dir"
DATA_PROCESSING_CLOSE_PRICE_GRAPH_FILE_NAME_KEY = "close_price_graph_file_name"
DATA_PROCESSING_50_MA_GRAPH_FILE_NAME_KEY = "50ma_graph_file_name"
DATA_PROCESSING_100_MA_GRAPH_FILE_NAME_KEY = "100ma_graph_file_name"
DATA_PROCESSING_200_MA_GRAPH_FILE_NAME_KEY = "200ma_graph_file_name"
DATA_PROCESSING_50_100_200_MA_COMP_GRAPH_FILE_NAME_KEY = "close_50_100_200_ma_comp_graph_file_name"

# Model Training Related Constants
MODEL_TRAINING_CONFIG_KEY = "model_training_config"
MODEL_TRAINING_DATA_DIR_KEY = "model_training_data_dir"
MODEL_TRAINING_TRAIN_DATA_FILE_NAME_KEY = "model_train_data_file_name"
MODEL_TRAINING_TEST_DATA_FILE_NAME_KEY = "model_test_data_file_name"
MODEL_TRAINING_MODEL_FILE_NAME_KEY = "model_file_name"

# Model Prediction Related Constants
MODEL_PREDICTION_CONFIG_KEY = "model_prediction_config"
MODEL_PREDICTION_DATA_DIR_KEY = "model_prediction_data_dir"
MODEL_PREDICTION_GRAPHS_DATA_DIR__NAME_KEY = "model_prediction_graphs_dir"
MODEL_PREDICTION_PREDICTED_GRAPH_FILE_NAME_KEY = "model_prediction_predicted_graph_file_name"