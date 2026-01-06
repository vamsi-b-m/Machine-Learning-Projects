from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtfifact",["ingested_data_file_path", "is_ingested", "message"])
DataCleaningArtifact = namedtuple("DataCleaningArtifact",["cleaned_data_file_path", "is_cleaned", "message"])
DataValidationArtifact = namedtuple("DataValidationArtifact", ["validated_data_file_path","report_file_path", "report_page_file_path", "is_validated", "message"])
DataManipulationArtifact = namedtuple("DataManipulationArtifact", ["processed_data_file_path", "processed_pickle_file_path", "similarity", "is_manipulated", "message"])
ModelGeneratorArtifact = namedtuple("ModelTrainingArtifact", ["posters_url_list", "model_generated_data_file_path", "is_generated", "message"])