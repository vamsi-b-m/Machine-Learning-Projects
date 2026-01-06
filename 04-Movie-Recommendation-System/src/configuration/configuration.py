import os, sys
from src.constant import *
from src.utils import *
from src.constant import *
from src.entity.config_entity import DataIngestionConfig, DataCleaningConfig, DataValidationConfig, DataManipulationConfig, ModelGeneratorConfig, TrainingPipelineConfig


class Configuration:

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH) -> None:
        try:
            self.config_file_path = config_file_path
            self.config_info = read_yaml_file(file_path=self.config_file_path)
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
                DATA_INGESTION_ARTIFACT_DIR
            )
            
            kaggle_dataset_url = data_ingestion_config_info[DATA_INGESTION_KAGGLE_DATASET_URL_KEY]
            zip_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_ZIP_DATA_DIR_KEY])
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR])

            data_ingestion_config = DataIngestionConfig(kaggle_dataset_url=kaggle_dataset_url,
                                                        zip_data_dir=zip_data_dir,
                                                        ingested_data_dir=ingested_data_dir
                                                        )
            return data_ingestion_config
        except Exception as e:
            raise Exception(e, sys) from e
         
    def get_data_cleaning_config(self) -> DataCleaningConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_cleaning_config_info = self.config_info[DATA_CLEANING_CONFIG_KEY]
            data_cleaning_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                DATA_CLEANING_ARTIFACT_DIR
            )
            cleaned_data_dir = os.path.join(data_cleaning_artifact_dir, data_cleaning_config_info[DATA_CLEANING_CLEANED_DATA_DIR])
            cleaned_data_file_name = data_cleaning_config_info[DATA_CLEANING_CLEANED_DATA_FILE_NAME]
            cleaned_data_file_path = os.path.join(cleaned_data_dir, cleaned_data_file_name)

            data_cleaning_config = DataCleaningConfig(cleaned_data_dir=cleaned_data_dir, cleaned_data_file_path=cleaned_data_file_path)
            return data_cleaning_config
        except Exception as e:
            raise Exception(e, sys) from e

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                DATA_VALIDATION_ARTIFACT_DIR
            )

            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            schema_config = self.config_info[SCHEMA_CONFIG_KEY]

            schema_file_path = os.path.join(
                ROOT_DIR,
                schema_config[SCHEMA_DIR_KEY],
                schema_config[SCHEMA_FILE_NAME_KEY]
            )

            report_file_dir = os.path.join(
                ROOT_DIR,
                data_validation_artifact_dir,
                DATA_VALIDATION_REPORT_FILE_DIR
            )

            report_file_path = os.path.join(
                report_file_dir,
                data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(
                data_validation_artifact_dir,
                data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            validated_data_dir = os.path.join(data_validation_artifact_dir, 
                                              data_validation_config[DATA_VALIDATION_VALIDATED_DATA_DIR_KEY]
                                              )
            validated_data_file_path = os.path.join(validated_data_dir, data_validation_config[DATA_VALIDATION_VALIDATED_DATA_FILE_NAME])

            data_validation_config = DataValidationConfig(
                                                        validated_data_dir=validated_data_dir,
                                                        validated_data_file_path=validated_data_file_path,
                                                        report_file_dir=report_file_dir,
                                                        schema_file_path=schema_file_path, 
                                                        report_file_path=report_file_path, 
                                                        report_page_file_path=report_page_file_path
                                                        )
            return data_validation_config
        
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_data_manipulation_config(self) -> DataManipulationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_manipulation_artifact_dir = os.path.join(
                artifact_dir,
                self.time_stamp,
                DATA_MANIPULATION_ARTIFACT_DIR
            )

            data_manipulation_config = self.config_info[DATA_MANIPULATION_CONFIG_KEY]

            processed_data_dir = os.path.join(data_manipulation_artifact_dir, data_manipulation_config[DATA_MANIPULATION_PROCESSED_DATA_DIR])
            processed_data_file_path = os.path.join(processed_data_dir, data_manipulation_config[DATA_MANIPULATION_PROCESSED_DATA_FILE_NAME])

            processed_pickle_data_dir = os.path.join(data_manipulation_artifact_dir, data_manipulation_config[DATA_MANIPULATION_PICKLE_FILE_DIR])
            processed_pickle_file_name = data_manipulation_config[DATA_MANIPULATION_PROCESSED_PICKLE_FILE_NAME]
            processed_pickle_file_path = os.path.join(processed_pickle_data_dir, processed_pickle_file_name)

            data_manipulation_config = DataManipulationConfig(processed_data_dir=processed_data_dir,
                                                              processed_data_file_path=processed_data_file_path,
                                                              processed_pickle_data_dir=processed_pickle_data_dir,
                                                              processed_pickle_file_path=processed_pickle_file_path
                                                              )
            return data_manipulation_config
        except Exception as e:
            raise Exception(e, sys) from e  

    def get_model_generator_config(self) -> ModelGeneratorConfig:
        try:
            model_dir = os.path.join(ROOT_DIR, MODEL_DIR)

            model_generation_dir = os.path.join(model_dir, MODEL_GENERATOR_ARTIFACT_DIR)

            model_generation_config = self.config_info[MODEL_GENERATOR_CONFIG_KEY]

            model_generated_data_dir = os.path.join(model_generation_dir, model_generation_config[MODEL_GENERATOR_GENERATED_DATA_DIR])
            model_generated_data_file_name = model_generation_config[MODEL_GENERATOR_GENERATED_DATA_FILE_NAME]
            model_generated_data_file_path = os.path.join(model_generated_data_dir, model_generated_data_file_name)

            model_generation_config = ModelGeneratorConfig(model_generated_data_dir=model_generated_data_dir,
                                                           model_generated_data_file_path=model_generated_data_file_path)
            return model_generation_config
        except Exception as e:
            raise Exception(e, sys) from e

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
        artifact_dir = os.path.join(ROOT_DIR , DATA_DIR, training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
        training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)

        print("\n*20",self.time_stamp,"\n*20")
        return training_pipeline_config