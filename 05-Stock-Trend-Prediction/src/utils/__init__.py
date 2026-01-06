import os, sys
import yaml

import pandas as pd

def read_yaml_file(file_path:str):
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Exception(e, sys) from e
    
def read_csv_file(file_path:str):
    try:
        dataset = pd.read_csv(file_path)
        return dataset
    except Exception as e:
        raise Exception(e, sys) from e
    
def write_csv_file(dataset: pd.DataFrame, file_path:str):
    try:
        dataset.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(e, sys) from e