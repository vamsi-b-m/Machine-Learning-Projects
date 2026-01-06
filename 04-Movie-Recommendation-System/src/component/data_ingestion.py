import os, shutil
import sys
import logging
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        """
        Initialize the DataIngestion instance.
        Args:
            config (DataIngestionConfig): Configuration for data ingestion.
        """
        self.data_ingestion_config = data_ingestion_config
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    def download_zip_file(self):
        """
        Download the dataset from Kaggle.
        Returns:
            str: Path to the downloaded zip file.
        """
        try:
            api = KaggleApi()
            api.authenticate()
            
            dataset_url = self.data_ingestion_config.kaggle_dataset_url
            zip_data_dir = self.data_ingestion_config.zip_data_dir

            os.makedirs(zip_data_dir, exist_ok=True)
            self.logger.info("Downloading dataset from Kaggle repo %s.", dataset_url)
            api.dataset_download_files(dataset=dataset_url, path=zip_data_dir, unzip=False)

            file_name = os.listdir(zip_data_dir)[0]
            zip_file_path = os.path.join(zip_data_dir, file_name)

            self.logger.info("Dataset downloaded successfully.")
            return zip_file_path

        except Exception as e:
            self.logger.exception(f"Error downloading dataset: {str(e)}")
            raise

    def extract_dataset(self, zip_file_path: str):
        """
        Extract the dataset from the zip file.
        Args:
            zip_file_path (str): Path to the zip file.
        Returns:
            str: Path to the extracted dataset.
        """
        try:
            ingested_data_dir = self.data_ingestion_config.ingested_data_dir

            # if os.path.exists(ingested_data_dir):
            #     os.remove(ingested_data_dir)

            os.makedirs(ingested_data_dir, exist_ok=True)

            self.logger.info("Extracting dataset...")
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(ingested_data_dir)

            ingested_dataset_name = os.listdir(ingested_data_dir)[0]
            ingested_dataset_path = os.path.join(ingested_data_dir, ingested_dataset_name)

            self.logger.info("Dataset Extracted and Ingested successfully at %s.", ingested_dataset_path)
            return ingested_dataset_path

        except Exception as e:
            self.logger.exception(f"Error extracting dataset: {str(e)}")
            raise

    def ingest_data(self):
        """
        Ingest the data by downloading and extracting the dataset.
        Returns:
            DataIngestionArtifact: Artifact containing information about the ingestion process.
        """
        try:
            zip_file_path = self.download_zip_file()
            dataset_path = self.extract_dataset(zip_file_path)
            artifact = DataIngestionArtifact(
                ingested_data_file_path=dataset_path,
                is_ingested=True,
                message="Data ingestion completed successfully."
            )
            return artifact

        except Exception as e:
            self.logger.exception(f"Data ingestion failed: {str(e)}")
            raise

    def initiate_data_ingestion(self):
        """
        Initiate the data ingestion process by downloading and extracting the dataset.
        Returns:
            DataIngestionArtifact: Artifact containing information about the ingestion process.
        """
        try:
            self.logger.info("Data ingestion process initiated.")
            data_ingestion_artifact = self.ingest_data()
            self.logger.info("Data ingestion process completed.\n")
            return data_ingestion_artifact

        except Exception as e:
            self.logger.exception(f"Data ingestion process failed: {str(e)}\n")
            raise
