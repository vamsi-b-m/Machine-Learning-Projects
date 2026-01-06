import os, sys
import logging

import pandas as pd
import numpy as np

from src.utils import *
from src.entity.config_entity import ModelTrainingConfig
from src.entity.artifact_entity import DataProcessingArtifact, ModelTrainingArtifact

from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

class ModelTraining:

    def __init__(self, model_training_config:ModelTrainingConfig, data_processing_artifact:DataProcessingArtifact) -> None:
        try:
            self.model_training_config = model_training_config
            self.data_processing_artifact = data_processing_artifact
        except Exception as e:
            raise Exception(e, sys) from e
    
    def train_test_split(self):
        try:
            # Dividing the dataset into Train and Test
            self.train_dataset = pd.DataFrame({'Date': self.dataset['Date'], 'Close': self.dataset['Close']}).iloc[:int(len(self.dataset)*0.70)]
            self.test_dataset = pd.DataFrame({'Date': self.dataset['Date'], 'Close': self.dataset['Close']}).iloc[int(len(self.dataset)*0.70):int(len(self.dataset))]

            model_training_data_dir_path = self.model_training_config.model_training_data_dir_path
            os.makedirs(model_training_data_dir_path, exist_ok=True)

            train_data_file_path = self.model_training_config.model_train_data_file_path
            test_data_file_path = self.model_training_config.model_test_data_file_path

            write_csv_file(dataset=self.train_dataset, file_path=train_data_file_path)
            write_csv_file(dataset=self.test_dataset, file_path=test_data_file_path)

            return train_data_file_path, test_data_file_path
        
        except Exception as e:
            raise Exception(e, sys) from e 

    def feature_scaling(self):
        try:
            self.train_scaler = MinMaxScaler(feature_range=(0,1))
            self.data_train_arr = self.train_scaler.fit_transform(pd.DataFrame(self.train_dataset['Close']))

            self.x_train = []
            self.y_train = []

            for i in range(100, self.data_train_arr.shape[0]):
                self.x_train.append(self.data_train_arr[i-100:i])
                self.y_train.append(self.data_train_arr[i, 0])

            self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)

        except Exception as e:
            raise Exception(e, sys) from e

    def train_model(self):
        try:
            self.model_file_path = self.model_training_config.model_file_path

            if not os.path.exists(self.model_file_path):

                from keras.layers import Dense, Dropout, LSTM
                from keras.models import Sequential


                self.model = Sequential()

                # Layer 1
                self.model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(self.x_train.shape[1],1)))
                self.model.add(Dropout(0.2))

                # Layer 2
                self.model.add(LSTM(units=60, activation='relu', return_sequences=True))
                self.model.add(Dropout(0.3))

                # Layer 3
                self.model.add(LSTM(units=80, activation='relu', return_sequences=True))
                self.model.add(Dropout(0.4))

                # Layer 4
                self.model.add(LSTM(units=120, activation='relu'))
                self.model.add(Dropout(0.5))

                # Layer 5
                self.model.add(Dense(units=1))

                # Summary Generation
                model_summary = self.model.summary()

                print(model_summary)

                self.model.compile(optimizer="adam", loss='mean_squared_error')
                self.model.fit(self.x_train, self.y_train, epochs=50)

                self.model.save(self.model_file_path)
                print(self.model_file_path)
            else:
                print(self.model_file_path)

        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_model_training_config(self):
        try:
            processed_data_file_path = self.data_processing_artifact.processed_data_file_path
            self.dataset = read_csv_file(file_path=processed_data_file_path)
            train_data_file_path, test_data_file_path = self.train_test_split()
            self.feature_scaling()
            self.train_model()

            model_training_artifact = ModelTrainingArtifact(
                processed_data_file_path = processed_data_file_path,
                train_data_file_path = train_data_file_path,
                test_data_file_path = test_data_file_path,
                model_file_path = self.model_file_path,
                train_scaler = self.train_scaler,
                y_train = self.y_train,
                is_trained="True",
                message="Model Training Completed"
            )
            return model_training_artifact
        except Exception as e:
            raise Exception(e, sys) from e
        
    def initiate_model_training(self) -> ModelTrainingArtifact:
        try:
            model_training_artifact = self.get_model_training_config()
            return model_training_artifact
        except Exception as e:
            raise Exception(e, sys) from e