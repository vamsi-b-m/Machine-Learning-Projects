import os
import sys
import json
import pickle
import logging

import pandas as pd

from src.utils import load_data, save_data

from src.entity.config_entity import DataManipulationConfig
from src.entity.artifact_entity import DataValidationArtifact, DataManipulationArtifact

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DataManipulation:
    
    def __init__(self, data_manipulation_config: DataManipulationConfig, data_validation_artifact:DataValidationArtifact) -> None:
        try:
            self.data_manipulation_config = data_manipulation_config
            self.data_validation_artifact = data_validation_artifact
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            raise Exception(e, sys) from e
        
    def read_data(self):
        try:
            validated_data_file_path = self.data_validation_artifact.validated_data_file_path
            self.validated_data = load_data(file_path=validated_data_file_path)
            self.logger.info("Data loaded successfully from %s", validated_data_file_path)
        except Exception as e:
            raise Exception(e, sys) from e
        
    def feature_engineering_and_selection(self):
        try:
            self.validated_data['year'] = self.validated_data['date_x'].apply(lambda x: str(x).split("/")[2].split()[0])
            self.validated_data['year'] = self.validated_data['year'].astype(int)
            self.logger.info("Year column created successfully")
            self.validated_data = self.validated_data[['names', 'overview', 'genre', 'year']]
            self.logger.info("Selected the required features to train the model")

            self.logger.info("Performing One-Hot-Encoding on genre feature and dropping it")
            unique_genres = {genre.strip().replace(" ", "_") for movie in self.validated_data['genre'] for genre in movie.split(',')}
            for genre in unique_genres:
                self.validated_data[genre] = self.validated_data['genre'].str.contains(genre).astype(int)
            self.validated_data = self.validated_data.drop(columns=['genre'], axis=1)
            self.logger.info("The new features created are : %s", unique_genres)

        except Exception as e:
            self.logger.exception("Error occurred during creating year column", exc_info=True)
            raise Exception(e, sys) from e
        
    def save_processed_data(self):
        try:
            processed_data_dir = self.data_manipulation_config.processed_data_dir
            os.makedirs(processed_data_dir, exist_ok=True)
            self.processed_data = self.validated_data 
            processed_data_file_path = self.data_manipulation_config.processed_data_file_path
            save_data(self.processed_data, file_path=processed_data_file_path)
            self.logger.info("Data saved successfully to %s", processed_data_file_path)
            return processed_data_file_path
        except Exception as e:
            self.logger.exception("Error occurred during saving data", exc_info=True)
            raise Exception(e, sys) from e
        
    def save_pickle_file(self):
        try:
            pickle_data_dir = self.data_manipulation_config.processed_pickle_data_dir
            os.makedirs(pickle_data_dir, exist_ok=True)
            processed_pickle_data_file_path = self.data_manipulation_config.processed_pickle_file_path
            pickle.dump(self.processed_data, open(processed_pickle_data_file_path, "wb"))
            self.logger.info("Pickle file saved successfully to %s", processed_pickle_data_file_path)
            return processed_pickle_data_file_path
        except Exception as e:
            self.logger.exception("Error occurred during saving the pickle file", exc_info=True)
            raise Exception(e, sys) from e
        
    def vectorization(self):
        try:
            self.logger.info("Performing Vectorization on 'overview' column")
            cv =  CountVectorizer(max_features=self.processed_data.shape[0], stop_words="english")
            vector = cv.fit_transform(self.processed_data['overview'].values.astype('U')).toarray()
            self.logger.info("Shape of the vector %s", vector.shape)
            self.logger.info("Calculating cosine similarity for the vector")
            similarity = cosine_similarity(vector)

            return vector, similarity
        except Exception as e:
            raise Exception(e, sys) from e

    def initiate_data_manipulation(self):
        try:
            self.is_manipulated = False
            self.read_data()
            self.feature_engineering_and_selection()
            processed_data_file_path = self.save_processed_data()
            processed_pickle_data_file_path = self.save_pickle_file()
            vector, similarity = self.vectorization()
            self.is_manipulated = True
            return DataManipulationArtifact(processed_data_file_path=processed_data_file_path, 
                                            processed_pickle_file_path=processed_pickle_data_file_path,
                                            similarity=similarity,
                                            is_manipulated=self.is_manipulated,
                                            message="Data Manipulation Completed")
        except Exception as e:
            raise Exception(e, sys) from e