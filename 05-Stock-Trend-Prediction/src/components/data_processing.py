import os, sys
import logging

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import plotly.graph_objects as go

from src.utils import *
from src.entity.config_entity import DataProcessingConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataPreprocessingArtifact, DataProcessingArtifact


class DataProcessing:

    def __init__(self, data_processing_config:DataProcessingConfig, data_ingestion_artifact:DataIngestionArtifact, data_preprocessing_artifact:DataPreprocessingArtifact) -> None:
        try:
            self.data_processing_config = data_processing_config
            self.data_preprocessing_artifact = data_preprocessing_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_moving_averages(self):
        try:
            self.ma50 = self.dataset['Close'].rolling(50).mean()
            self.ma100 = self.dataset['Close'].rolling(100).mean()
            self.ma200 = self.dataset['Close'].rolling(200).mean()

            self.processing_moving_averages_dir_path = self.data_processing_config.processing_moving_averages_dir_path
            os.makedirs(self.processing_moving_averages_dir_path, exist_ok=True)

            self.processing_fifty_moving_average_file_path = self.data_processing_config.processing_fifty_moving_average_file_path
            write_csv_file(self.ma50, self.processing_fifty_moving_average_file_path)

            self.processing_hundred_moving_average_file_path = self.data_processing_config.processing_hundred_moving_average_file_path
            write_csv_file(self.ma100, self.processing_hundred_moving_average_file_path)

            self.processing_two_hundred_moving_average_file_path = self.data_processing_config.processing_two_hundred_moving_average_file_path
            write_csv_file(self.ma200, self.processing_two_hundred_moving_average_file_path)

            self.processing_close_price_graph_file_path = self.data_processing_config.processing_close_price_graph_file_path
            os.makedirs(os.path.dirname(self.processing_close_price_graph_file_path), exist_ok=True)

            self.processing_50_ma_graph_file_path = self.data_processing_config.processing_50_ma_graph_file_path
            os.makedirs(os.path.dirname(self.processing_50_ma_graph_file_path), exist_ok=True)

            self.processing_100_ma_graph_file_path = self.data_processing_config.processing_100_ma_graph_file_path
            os.makedirs(os.path.dirname(self.processing_100_ma_graph_file_path), exist_ok=True)

            self.processing_200_ma_graph_file_path = self.data_processing_config.processing_200_ma_graph_file_path
            os.makedirs(os.path.dirname(self.processing_200_ma_graph_file_path), exist_ok=True)

            self.processing_50_100_200_ma_comp_graph_file_path = self.data_processing_config.processing_50_100_200_ma_comp_graph_file_path
            os.makedirs(os.path.dirname(self.processing_50_100_200_ma_comp_graph_file_path), exist_ok=True)

        except Exception as e:
            raise Exception(e, sys) from e
        
    def generate_graphs(self):
        try:
            stock_name = self.data_ingestion_artifact.stock_symbol[:-3]
            date_range = pd.to_datetime(self.dataset['Date'])
            
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=self.dataset['Date'], y=self.dataset['Close'], name="Close Price"))
            # Update layout to position legend inside the graph
            fig.update_layout(
                title=f"{stock_name} Close Price",
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
            fig.update_traces(hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: %{y}')
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=pd.date_range(start=date_range.min(), end=date_range.max(), freq='YS').tolist(), tickformat='%Y'))
            fig.write_html(self.processing_close_price_graph_file_path)


            fig.add_trace(go.Scatter(x=self.dataset['Date'], y=self.ma50, name="ma50"))
            # Update layout to position legend inside the graph
            fig.update_layout(
                title=f"{stock_name} ma50",
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
            fig.update_traces(hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: %{y}')
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=pd.date_range(start=date_range.min(), end=date_range.max(), freq='YS').tolist(), tickformat='%Y'))
            fig.write_html(self.processing_50_ma_graph_file_path)


            fig.add_trace(go.Scatter(x=self.dataset['Date'], y=self.ma100, name="ma100"))
            # Update layout to position legend inside the graph
            fig.update_layout(
                title=f"{stock_name} ma100",
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
            fig.update_traces(hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: %{y}')
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=pd.date_range(start=date_range.min(), end=date_range.max(), freq='YS').tolist(), tickformat='%Y'))
            fig.write_html(self.processing_100_ma_graph_file_path)


            fig.add_trace(go.Scatter(x=self.dataset['Date'], y=self.ma200, name="ma200"))
            # Update layout to position legend inside the graph
            fig.update_layout(
                title=f"{stock_name} ma's Comparision",
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

            fig.update_traces(hovertemplate='Date: %{x|%Y-%m-%d}<br>Price: %{y}')
            fig.update_layout(xaxis=dict(tickmode='array', tickvals=pd.date_range(start=date_range.min(), end=date_range.max(), freq='YS').tolist(), tickformat='%Y'))
            fig.write_html(self.processing_200_ma_graph_file_path)


        except Exception as e:
            print("Error:", e)

    def get_processed_data(self):
        try:
            preprocessed_data_file_path = self.data_preprocessing_artifact.preprocessed_data_file_path
            self.dataset = read_csv_file(preprocessed_data_file_path)
            
            processed_data_file_path  = self.data_processing_config.processing_data_file_path
            processed_data_file_dir = os.path.dirname(processed_data_file_path)
            os.makedirs(processed_data_file_dir, exist_ok=True)

            self.dataset['Date'] = pd.to_datetime(self.dataset['Date'])
            self.dataset = self.dataset[['Date', 'Close']]
            self.dataset = self.dataset.reset_index()
            self.dataset.to_csv(processed_data_file_path, index=False, date_format='%Y-%m-%d')
            self.dataset = read_csv_file(processed_data_file_path)

            self.get_moving_averages()
            processed_graphs_file_path = self.generate_graphs()

            is_processed = True
            message = "Data Processing Completed"

            data_processing_artifact = DataProcessingArtifact(
                processed_data_file_path = processed_data_file_path,
                processing_close_price_graph_file_path = self.processing_close_price_graph_file_path,
                processing_50_ma_graph_file_path = self.processing_50_ma_graph_file_path,
                processing_100_ma_graph_file_path = self.processing_100_ma_graph_file_path,
                processing_200_ma_graph_file_path = self.processing_200_ma_graph_file_path,
                #processing_50_100_200_ma_comp_graph_file_path = self.processing_50_100_200_ma_comp_graph_file_path,
                is_processed=is_processed,
                message=message
            )

            return data_processing_artifact
        
        except Exception as e:
            raise Exception(e, sys) from e
        
    def initiate_data_processing(self) -> DataProcessingArtifact:
        try:
            data_processing_artifact = self.get_processed_data()
            return data_processing_artifact
        except Exception as e:
            raise Exception(e, sys) from e