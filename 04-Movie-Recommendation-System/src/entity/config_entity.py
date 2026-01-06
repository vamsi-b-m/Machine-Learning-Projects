from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["kaggle_dataset_url", "zip_data_dir", "ingested_data_dir"])
DataCleaningConfig = namedtuple("DataCleaningConfig", ["cleaned_data_dir", "cleaned_data_file_path"])
DataValidationConfig = namedtuple("DataValidationConfig", ["validated_data_dir", "validated_data_file_path", "schema_file_path", "report_file_dir", "report_file_path", "report_page_file_path"])
DataManipulationConfig = namedtuple("DataManipulationConfig", ["processed_data_dir", "processed_data_file_path", "processed_pickle_data_dir", "processed_pickle_file_path"])
ModelGeneratorConfig = namedtuple("ModelGeneratorConfig", ["model_generated_data_dir", "model_generated_data_file_path"])
ModelPusherConfig = namedtuple("ModelTrainingConfig", [])
TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])
