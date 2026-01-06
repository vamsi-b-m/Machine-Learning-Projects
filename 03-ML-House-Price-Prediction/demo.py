from housing.pipeline.pipeline import Pipeline
from housing.logger import logging
from housing.config.configuration import Configuration
from housing.components.data_transformer import DataTransformation

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
        # data_validation_config = Configuration()
        # print(data_validation_config.get_data_validation_config())
        # schema_file_path = r"/Users/vambat1/Documents/Projects/Machine-Learning/03-ML-House-Price-Prediction/config/schema.yml"
        # file_path = r"/Users/vambat1/Documents/Projects/Machine-Learning/03-ML-House-Price-Prediction/housing/artifact/data_ingestion/2023-12-11-23-50-43/ingested_data/train/housing.csv"
        # df = DataTransformation.load_data(file_path=file_path, schema_file_path=schema_file_path)
        # print(df.columns)
        # print(df.dtypes)
    except Exception as e:
        logging.error(f"{e}")
        print("Exception : ", e)

if __name__ == "__main__":
    main()