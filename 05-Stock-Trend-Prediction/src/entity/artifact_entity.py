from collections import namedtuple

DataIngestionArtifact = namedtuple('DataIngestionArtifact', ["ingested_data_file_path", "stock_symbol", "is_ingested", "message"])
DataPreprocessingArtifact = namedtuple('DataPreprocessingArtifact', ["preprocessed_data_file_path", "is_preprocessed", "message"])
DataProcessingArtifact = namedtuple("DataProcessingArtifact", ["processed_data_file_path", 
                                                               "processing_close_price_graph_file_path",
                                                               "processing_50_ma_graph_file_path",
                                                               "processing_100_ma_graph_file_path",
                                                               "processing_200_ma_graph_file_path",
                                                               "is_processed", 
                                                               "message"])

ModelTrainingArtifact = namedtuple("ModelTrainingArtifact", ["processed_data_file_path", 
                                                             "train_data_file_path", 
                                                             "test_data_file_path", 
                                                             "model_file_path", 
                                                             "train_scaler", 
                                                             "y_train",
                                                             "is_trained",
                                                             "message"])

ModelPredictionArtifact = namedtuple("ModelPredictionArtifact", ["model_prediction_predicted_graph_file_path",
                                                                 "is_predicted",
                                                                 "message"])