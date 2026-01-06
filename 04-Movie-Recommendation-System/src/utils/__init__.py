import os
import sys
import yaml
import dill

import pandas as pd


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Exception(e, sys) from e
    
def load_data(file_path:str) -> pd.DataFrame:
    try:
        dataframe = pd.read_csv(file_path)
        return dataframe
    except Exception as e:
        raise Exception(e, sys) from e
    
def save_data(data, file_path: str):
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(e, sys) from e
    
def save_object(file_path: str, obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise Exception(e, sys) from e
    
def load_object(file_path: str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise Exception(e, sys) from e