from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", ["ingested_data_file_path"])
DataPreprocessingConfig = namedtuple("DataPreprocessingConfig", ["preprocessing_data_file_path"])
DataProcessingConfig = namedtuple("DataProcessingConfig", 
                                  ["processing_data_file_path", 
                                   "processing_moving_averages_dir_path", 
                                   "processing_fifty_moving_average_file_path", 
                                   "processing_hundred_moving_average_file_path", 
                                   "processing_two_hundred_moving_average_file_path", 
                                   "processing_close_price_graph_file_path",
                                   "processing_50_ma_graph_file_path",
                                   "processing_100_ma_graph_file_path",
                                   "processing_200_ma_graph_file_path",
                                   "processing_50_100_200_ma_comp_graph_file_path"
                                   ])

ModelTrainingConfig = namedtuple("ModelTrainingConfig", ["model_training_data_dir_path", "model_train_data_file_path", "model_test_data_file_path", "model_file_path"])
ModelPredictionConfig = namedtuple("ModelPredictionConfig", ["model_prediction_predicted_graph_file_path"])



TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])