import os
import sys
import random
import logging
import requests

import pandas as pd

from src.utils import load_data
from src.constant import *

from src.entity.config_entity import ModelGeneratorConfig
from src.entity.artifact_entity import DataManipulationArtifact, ModelGeneratorArtifact

class ModelGenerator:

    def __init__(self, movie_name, movie_genre, model_generation_config: ModelGeneratorConfig, data_manipulation_artifact: DataManipulationArtifact) -> None:
        try:
            self.model_generation_config = model_generation_config
            self.data_manipulation_artifact = data_manipulation_artifact
            self.similarity = self.data_manipulation_artifact.similarity
            self.movie_name = movie_name
            self.target_genre = movie_genre
            self.logger = logging.getLogger(__name__)
            self.logger.info("ModelTrainer initialized.")
        except Exception as e:
            self.logger.error(f"Error initializing ModelTrainer: {e}")
            raise Exception(e, sys) from e

    def read_data(self):
        try:
            processed_data_file_path = self.data_manipulation_artifact.processed_data_file_path
            self.logger.info(f"Reading data from file: {processed_data_file_path}")
            self.processed_data = load_data(file_path=processed_data_file_path)
            self.logger.info("Data read successfully.")
        except Exception as e:
            self.logger.error(f"Error reading data: {e}")
            raise Exception(e, sys) from e

    def recommend_with_movie_name(self, movie_name, movie_count_to_recommend):
        try:
            movies_recommended = []
            self.logger.info(f"Recommendation based on movie name : {movie_name}")
            index = self.processed_data[self.processed_data['names']==movie_name].index[0]
            distances = sorted(list(enumerate(self.similarity[index])), reverse=True, key=lambda vector: vector[1])
            
            for movie in distances[0:movie_count_to_recommend]:
                movies_recommended.append(self.processed_data.iloc[movie[0]].names)
                
            self.logger.info(f"Recommended the following the movies : {movies_recommended}")
            return movies_recommended
        except Exception as e:
            self.logger.error(f"Error recommending with movie name: {e}")
            raise Exception(e, sys) from e

    def recommend_with_genre(self, target_genre):
        try:
            self.logger.info("Initiating recommendation based on genre.")
            # Define start column index and target genre
            start_column_index = 3
            movie_names = []
            
            for movie_index in range(len(self.processed_data)):
                movie_row = self.processed_data.iloc[movie_index, start_column_index:]
                if movie_row[target_genre] and not movie_row[movie_row.index != target_genre].any():
                    movie_names.append(self.processed_data.iloc[movie_index]['names'])

            movie_count = len(movie_names)
            self.logger.info(f"Only {movie_count} movies are available based on genre : {target_genre}")
            if movie_count < 15:
                self.logger.info(f"Since the movie count is less than 15 based on genre, Started Recommending based on the movie name")
                if movie_count == 0:
                    random_movie_name = random.choice(self.processed_data['names'])
                    self.logger.info("Since the movie count with genre %s is 0, recommending based in some random movie name : %s ", target_genre, random_movie_name)
                    recommended_movies_by_name = self.recommend_with_movie_name(random_movie_name, movie_count_to_recommend=15)
                    movies_recommended = recommended_movies_by_name
                    self.logger.info(f"Recommended the following the movies based on a random movie : {movies_recommended}")
                else:
                    movie_count_to_recommend = 15 - movie_count
                    self.logger.info(f"Started recommend_with_movie_name to fetch movies based on the random movie from genre movie list")
                    movie_name = random.choice(movie_names)
                    recommended_movies_by_name = self.recommend_with_movie_name(movie_name=movie_name, movie_count_to_recommend=movie_count_to_recommend)
                    movies_recommended = movie_names + recommended_movies_by_name

            else:
                movies_recommended = random.sample(movie_names, k=15)
                self.logger.info(f"Recommended movies based on genre: {movies_recommended}")
            return movies_recommended
        except Exception as e:
            error_message = f"Error recommending with genre: {e}"
            self.logger.error(error_message)
            raise Exception(error_message) from e

    def get_movie_recommendation(self, movie_name, target_genre):
        try:
            recommended_movies = []
            if movie_name:
                self.logger.info("Recommending based on the Movie name : %s", movie_name)
                recommended_movies = self.recommend_with_movie_name(movie_name=movie_name, movie_count_to_recommend=15)
            elif target_genre:
                self.logger.info("Recommending based on the Movie Genre : %s", target_genre)
                recommended_movies = self.recommend_with_genre(target_genre=target_genre)
            else:
                pass

            return recommended_movies

        except Exception as e:
            raise Exception(e, sys) from e
    
    def fetch_movie_posters(self, recommended_movies):
        """
        Fetches movie posters for the recommended movies and saves them to the specified path.

        Args:
            recommended_movies (list): A list of movie names.
            save_path (str): Path to save the downloaded posters.

        Returns:
            None
        """
        try:
            api_key = 'b1f9d8f7'
            base_url = 'http://www.omdbapi.com/'

            posters_url_list = []
            for movie_name in recommended_movies:
                params = {
                    'apikey': api_key,
                    't': movie_name
                }

                response = requests.get(base_url, params=params)
                data = response.json()

                if response.status_code != 200:
                    print(f"Failed to fetch data for {movie_name}. Status code: {response.status_code}")
                    continue

                if 'Error' in data:
                    print(f"Error: {data['Error']}")
                    continue

                poster_url = data.get('Poster', 'N/A')
                if poster_url == 'N/A':
                    print(f"No poster available for {movie_name}")
                else:
                    posters_url_list.append(poster_url)

            return posters_url_list 
        except Exception as e:
            raise Exception(e, sys) from e

    def write_to_csv(self, recommended_movies):
        try:
            model_generated_data_dir = self.model_generation_config.model_generated_data_dir
            os.makedirs(model_generated_data_dir, exist_ok=True)
            model_generated_data_file_path = self.model_generation_config.model_generated_data_file_path
            
            # Check if file exists
            if not os.path.isfile(model_generated_data_file_path):
                # If file does not exist, create it with column names
                header = ["Serial"] + [f"Movie-{i}" for i in range(1, 16)]
                df = pd.DataFrame(columns=header)
                df.to_csv(model_generated_data_file_path, index=False)  # Initially write without index
                max_index = 0  # Start with index 1
            else:
                # Read the existing file to determine the maximum index
                df = pd.read_csv(model_generated_data_file_path)
                max_index = df.index.max() + 1  # Get the next available index

            # Add Serial column if it doesn't exist
            if "Serial" not in df.columns:
                df.insert(0, "Serial", range(1, len(df) + 1))

            # Append data to the CSV file with the correct index
            df = pd.DataFrame([recommended_movies], index=[max_index])
            df.to_csv(model_generated_data_file_path, mode='a', header=False)  # Append without header

            self.logger.info(f"Successfully wrote recommended movies to CSV: {model_generated_data_file_path}")
            return model_generated_data_file_path
        except Exception as e:
            error_msg = f"Error occurred while writing recommended movies to CSV: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from e

    def initiate_model_training(self) -> ModelGeneratorArtifact:
        try:
            self.logger.info("Model Generation Process Started")
            self.read_data()
            recommended_movies = self.get_movie_recommendation(movie_name=self.movie_name, target_genre=self.target_genre)
            posters_url_list = self.fetch_movie_posters(recommended_movies=recommended_movies)
            model_generated_data_file_path = self.write_to_csv(recommended_movies=recommended_movies)
            is_generated = True
            model_generator_artifact = ModelGeneratorArtifact(posters_url_list=posters_url_list, model_generated_data_file_path=model_generated_data_file_path,
                                                            is_generated=is_generated,
                                                            message="Model Generation Completed Successfully")
            self.logger.info("Model Generation Process Completed\n")
            return model_generator_artifact
        except Exception as e:
            error_msg = f"Error during model training: {e}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from e
