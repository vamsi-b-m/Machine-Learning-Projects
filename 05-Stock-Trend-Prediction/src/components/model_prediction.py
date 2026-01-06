import os, sys
import logging

import pandas as pd
import numpy as np

from src.utils import *
from src.entity.config_entity import ModelPredictionConfig
from src.entity.artifact_entity import DataIngestionArtifact, ModelTrainingArtifact, ModelPredictionArtifact

from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go


class ModelPrediction:
    
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, model_training_artifact: ModelTrainingArtifact, model_prediction_config: ModelPredictionConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_prediction_config = model_prediction_config
            self.model_training_artifact = model_training_artifact
        except Exception as e:
            raise Exception(e, sys) from e

    def read_data(self):
        try:
            dataset_file_path = self.model_training_artifact.processed_data_file_path
            train_data_file_path = self.model_training_artifact.train_data_file_path
            test_data_file_path = self.model_training_artifact.test_data_file_path
            self.dataset = read_csv_file(dataset_file_path)
            self.train_dataset = read_csv_file(train_data_file_path)
            self.test_dataset = read_csv_file(test_data_file_path)
        except Exception as e:
            raise Exception(e, sys) from e

    def prediction(self):
        try:
            from keras.models import load_model
            
            self.model_file_path = self.model_training_artifact.model_file_path

            # Load the trained model
            self.model = load_model(self.model_file_path)
            
            # Get the last 100 days data from the train data
            past_100_days = self.train_dataset.tail(100)

            # Combine past_100_days with test_dataset
            final_dataframe = pd.concat([past_100_days, self.test_dataset], ignore_index=True)

            
            self.test_pred_scaler = MinMaxScaler(feature_range=(0,1))
            self.input_data = self.test_pred_scaler.fit_transform(pd.DataFrame(final_dataframe['Close']))

            self.x_test = []
            self.y_test = []

            for i in range(100, self.input_data.shape[0]):
                self.x_test.append(self.input_data[i-100:i])
                self.y_test.append(self.input_data[i, 0])

            self.x_test, self.y_test = np.array(self.x_test), np.array(self.y_test)

            # Making Predictions
            self.y_predicted = self.model.predict(self.x_test)

            # Reshape y_test to a 2D array
            self.y_test = self.y_test.reshape(-1, 1)
            self.y_test = self.test_pred_scaler.inverse_transform(self.y_test)

            self.y_predicted = self.test_pred_scaler.inverse_transform(self.y_predicted)

        except Exception as e:
            raise Exception(e, sys) from e
    
    def generate_graphs(self):
        try:
            stock_name = self.data_ingestion_artifact.stock_symbol[:-3]
            self.model_prediction_predicted_graph_file_path = self.model_prediction_config.model_prediction_predicted_graph_file_path
            os.makedirs(os.path.dirname(self.model_prediction_predicted_graph_file_path), exist_ok=True)
            self.train_scaler = self.model_training_artifact.train_scaler
            self.y_train = self.model_training_artifact.y_train

            graph_data = pd.DataFrame()
            graph_data['Test'] = pd.DataFrame(self.y_test)
            graph_data['Pred'] = pd.DataFrame(self.y_predicted)
            
            final_y_train = self.y_train.reshape(-1,1)
            final_y_train = np.append(np.array(self.train_dataset['Close'][:100]), self.train_scaler.inverse_transform(final_y_train))

            train_dates = pd.to_datetime(self.dataset['Date'][:len(final_y_train)])
            test_pred_dates = pd.to_datetime(self.dataset['Date'][len(final_y_train):])

            fig = go.Figure()

            # Plotting the first graph
            fig.add_trace(go.Scatter(x=train_dates, y=final_y_train, mode='lines', name='Training Data'))
            # Plotting the second graph with adjusted x-axis range
            fig.add_trace(go.Scatter(x=test_pred_dates, y=graph_data['Test'], mode='lines', name='Test Data'))
            fig.add_trace(go.Scatter(x=test_pred_dates, y=graph_data['Pred'], mode='lines', name='Predicted Data'))

            # Update layout
            fig.update_layout(
                title=f"{stock_name}",
                xaxis_title='Date',
                yaxis_title='Price (INR)',
                height=600,
                width=1350,
                legend=dict(
                    x=0.02,
                    y=0.98,
                    traceorder="normal",
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="black"
                    ),
                    bgcolor="LightSteelBlue",
                    bordercolor="Black",
                    borderwidth=2
                )
            )
            # Customizing hover information to show full date and price
            fig.update_traces(hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: %{y}')

            # Add tickvals and ticktext for x-axis to show every 1 year
            date_range = pd.to_datetime(self.dataset['Date'])
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=pd.date_range(start=date_range.min(), end=date_range.max(), freq='YS').tolist(), tickformat='%Y'))
            fig.write_html(self.model_prediction_predicted_graph_file_path)

            return self.model_prediction_predicted_graph_file_path
        except Exception as e:
            raise Exception(e, sys) from e
    
    def get_model_prediction_config(self):
        try:
            self.read_data()
            self.prediction()
            model_prediction_predicted_graph_file_path = self.generate_graphs()
            model_prediction_artifact = ModelPredictionArtifact(
                model_prediction_predicted_graph_file_path=model_prediction_predicted_graph_file_path,
                is_predicted="True",
                message="Model Prediction Completed"
            )
            return model_prediction_artifact
        except Exception as e:
            raise Exception(e, sys) from e

    def initiate_model_prediction(self) -> ModelPredictionArtifact:
        try:
            model_prediction_artifact = self.get_model_prediction_config()
            return model_prediction_artifact
        except Exception as e:
            raise Exception(e, sys) from e
