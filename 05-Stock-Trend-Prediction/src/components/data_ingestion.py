import os, sys
import logging

import yfinance
import pandas as pd

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    
    def __init__(self, stock_symbol, data_ingestion_config=DataIngestionConfig) -> None:
        try:
            self.stock_symbol = stock_symbol
            self.data_ingestion_config = data_ingestion_config
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        except Exception as e:
            raise Exception(e, sys) from e
        
    def get_stock_data(self):
        try:
            #self.stock_symbol = self.data_ingestion_config.stock_symbol
            stock = yfinance.Ticker(self.stock_symbol)
            dataset = stock.history(period='10y', interval='1d')
            dataset = pd.DataFrame(dataset)
            file_path = self.data_ingestion_config.ingested_data_file_path
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataset.to_csv(file_path)
            return file_path
        except OSError as e:
            print(f"Exception : {e}")
        except Exception as e:
            raise Exception(e, sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            ingested_data_file_path = self.get_stock_data()
            stock_symbol = self.stock_symbol
            is_ingested = True
            message = "Data Ingestion Completed Successfully"
            data_ingestion_artifact = DataIngestionArtifact(
                ingested_data_file_path=ingested_data_file_path,
                stock_symbol = stock_symbol,
                is_ingested = is_ingested,
                message = message
            )
            return data_ingestion_artifact
        except Exception as e:
            raise Exception(e, sys) from e