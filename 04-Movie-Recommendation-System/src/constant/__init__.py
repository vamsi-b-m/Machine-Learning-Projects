import os
from datetime import datetime

ROOT_DIR = os.getcwd() #to get current working directory
DATA_DIR = "data"
MODEL_DIR = "model"
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)
#CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# Training pipeline related varibales
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# Data Ingestion Constants
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_KAGGLE_DATASET_URL_KEY = "kaggle_dataset_url"
DATA_INGESTION_ZIP_DATA_DIR_KEY = "zip_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR = "ingested_data_dir"

# Data Cleaning Related Constants
DATA_CLEANING_CONFIG_KEY = "data_cleaning_config"
DATA_CLEANING_ARTIFACT_DIR = "data_cleaning"
DATA_CLEANING_CLEANED_DATA_DIR = "cleaned_data_dir"
DATA_CLEANING_CLEANED_DATA_FILE_NAME = "cleaned_data_file_name"

# Data Validation Related Variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR = "data_validation"
DATA_VALIDATION_REPORT_FILE_DIR = "report"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"
DATA_VALIDATION_VALIDATED_DATA_DIR_KEY = "validated_data_dir"
DATA_VALIDATION_VALIDATED_DATA_FILE_NAME = "validated_data_file_name"

# Schema Related Variables
SCHEMA_CONFIG_KEY = "schema_config"
SCHEMA_DIR_KEY = "schema_dir"
SCHEMA_FILE_NAME_KEY = "schema_file_name"

# Data Manipulation Related Variables
DATA_MANIPULATION_CONFIG_KEY = "data_manipulation_config"
DATA_MANIPULATION_ARTIFACT_DIR = "data_manipulation"
DATA_MANIPULATION_PROCESSED_DATA_DIR = "processed_data_dir"
DATA_MANIPULATION_PROCESSED_DATA_FILE_NAME = "processed_data_file_name"
DATA_MANIPULATION_PICKLE_FILE_DIR = "processed_pickle_data_dir" 
DATA_MANIPULATION_PROCESSED_PICKLE_FILE_NAME = "processed_data_pickle_file_name"

# Model Generator Related Variable
MODEL_GENERATOR_CONFIG_KEY = "model_generator_config"
MODEL_GENERATOR_ARTIFACT_DIR = "model_generation"
MODEL_GENERATOR_GENERATED_DATA_DIR = "generated_data_dir"
MODEL_GENERATOR_GENERATED_DATA_FILE_NAME = "generated_data_file_name"