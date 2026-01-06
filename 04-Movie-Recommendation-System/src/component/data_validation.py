import os
import sys
import json
import logging
import pandas as pd

from src.constant import *
from src.utils import load_data, read_yaml_file, save_data
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataCleaningArtifact, DataValidationArtifact

class DataValidation:
    
    def __init__(self, data_validation_config: DataValidationConfig, data_cleaning_artifact: DataCleaningArtifact) -> None:
        try:
            self.data_validation_config = data_validation_config
            self.data_cleaning_artifact = data_cleaning_artifact
            self.schema_info = read_yaml_file(self.data_validation_config.schema_file_path)
            self.logger = logging.getLogger(__name__)
            self.validation_results = {'null_values': None, 'duplicates': None, 'inconsistency_indices': None, 'schema_feature_missing': None, 'dataset_feature_extra': None, 'schema_feature_not_in_dataset': None, 'schema_feature_dtype_mismatch': None}
        except Exception as e:
            raise Exception(e, sys) from e

    def read_data(self):
        try:
            cleaned_data_file_path = self.data_cleaning_artifact.cleaned_data_file_path
            self.data = load_data(file_path=cleaned_data_file_path)
            self.logger.info("Data loaded successfully from %s", cleaned_data_file_path)
        except Exception as e:
            self.logger.exception("Error occurred while reading data", exc_info=True)
            raise

    def check_null_values(self) -> bool:
        try:
            self.validate_null_values = False
            rows_with_null = self.data[self.data.isnull().any(axis=1)]
            if not rows_with_null.empty:
                self.validation_results['null_values'] = list(rows_with_null.index)
                self.logger.warning("Found rows with null values: %s", self.validation_results['null_values'])
            else:
                self.logger.info("No rows with null values found.")
                self.validate_null_values = True
        except Exception as e:
            raise Exception(e, sys) from e

    def check_duplicates(self) -> bool:
        try:
            self.validate_duplicates = False
            duplicates = self.data[self.data.duplicated()]
            if not duplicates.empty:
                self.validation_results['duplicates'] = list(duplicates.index)
                self.logger.warning("Found duplicates: %s", self.validation_results['duplicates'])
            else:
                self.logger.info("No duplicates found.")
                self.validate_duplicates = True
        except Exception as e:
            raise Exception(e, sys) from e
    
    def check_consistency(self) -> bool:
        try:
            self.validate_consistency = False
            inconsistency_indices = [str(self.data.index[i]) + " Missing" for i in range(1, len(self.data.index)) if self.data.index[i] != self.data.index[i-1] + 1]
            if inconsistency_indices:
                self.validation_results['inconsistency_indices'] = inconsistency_indices
                self.logger.warning("Found inconsistency at the indexes: %s", self.validation_results['inconsistency_indices'])
            else:
                self.logger.info("No inconsistency found.")
                self.validate_consistency = True
        except Exception as e:
            raise Exception(e, sys) from e
        
    def check_outliers(self) -> bool:
        try:
            pass
        except Exception as e:
            raise Exception(e, sys) from e

    def validate_dataset_schema(self) -> bool:
        try:
            self.validate_schema = False
            schema_features = list(self.schema_info['columns'].keys())
            dataset_features = list(self.data.columns)

            if len(schema_features) > len(dataset_features):
                self.validation_results['schema_feature_missing'] = [feature for feature in schema_features if feature not in dataset_features]
                self.logger.info("Some features from schema are missing in the dataset.")
            elif len(dataset_features) > len(schema_features):
                self.validation_results['dataset_feature_extra'] = [feature for feature in dataset_features if feature not in schema_features]
                self.logger.info("Some features from dataset are not mentioned in the schema.")
            else:
                for feature in schema_features:
                    if feature not in dataset_features:
                        self.validation_results['schema_feature_not_in_dataset'] = feature
                        self.logger.info("Feature %s is not found in the dataset.", feature)
                    else:
                        if not self.schema_info['columns'][feature] == self.data[feature].dtype.name:
                            self.validation_results['schema_feature_dtype_mismatch'] = feature
                            self.logger.info("Schema feature %s has different dtype compared to dataset feature %s dtype.", feature, feature)
                else:
                    self.validate_schema = True
                    self.logger.info("All features mentioned in the schema are available in dataset.")

        except Exception as e:
            raise Exception(e, sys) from e
        
    def validation_status(self):
        try:
            validation_status = [self.validate_null_values, self.validate_duplicates, self.validate_consistency, self.validate_schema]

            if all(validation_status):
                is_validated = True
                self.logger.info("All Data validation checks completed successfully.")
            else:
                is_validated = False
                self.logger.warning("Data validation checks failed. Some checks were not passed.")

            return is_validated
        except Exception as e:
            self.logger.exception("Error occurred while determining data validation status", exc_info=True)
            raise

    def get_and_save_data_validation_report(self):
        try:
            report_file_dir = self.data_validation_config.report_file_dir
            report_file_path = self.data_validation_config.report_file_path
            os.makedirs(report_file_dir, exist_ok=True)
            with open(report_file_path, 'w') as report_file:
                json.dump(self.validation_results, report_file, indent=4)
            self.logger.info("Data validation report saved successfully at: %s", report_file_path)
            return report_file_path
        except Exception as e:
            self.logger.exception("Error occurred while saving data validation report", exc_info=True)
            raise Exception(e, sys) from e
    
    def save_validated_data(self):
        try:
            validated_data_dir = self.data_validation_config.validated_data_dir
            os.makedirs(validated_data_dir, exist_ok=True)

            validated_data_file_path = self.data_validation_config.validated_data_file_path
            save_data(self.data, file_path=validated_data_file_path)
            self.logger.info("Data saved successfully to %s", validated_data_file_path)
            return validated_data_file_path
        except Exception as e:
            self.logger.exception("Error occurred during saving data", exc_info=True)
            raise Exception(e, sys) from e


    def initiate_data_validation(self):
        try:
            self.logger.info("Data Validation Process Started.")
            self.read_data()
            self.check_null_values()
            self.check_duplicates()
            self.check_consistency()
            self.validate_dataset_schema()
            is_validated = self.validation_status()
            report_file_path = self.get_and_save_data_validation_report()
            validated_data_file_path = self.save_validated_data()
            data_validation_artifact = DataValidationArtifact(
                validated_data_file_path=validated_data_file_path, 
                report_file_path=report_file_path, report_page_file_path="", 
                is_validated=is_validated, 
                message="Data Validation Completed Successfully"
                )
            self.logger.info("Data Validation Process Completed.\n")
            return data_validation_artifact
        except Exception as e:
            raise Exception(e, sys) from e
