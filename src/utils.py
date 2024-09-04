import yaml
import os
import logging
import time
import pandas as pd 
from datetime import datetime

# ===== READ/WRITE DATA FORMAT =====
def read_yaml(file_path):
  with open(file_path, 'r') as file:
    data = yaml.safe_load(file)
  return data

def dict_to_pd(dict_content:dict) -> pd.DataFrame: 
  df = pd.DataFrame(dict_content)
  return df

def get_second(time_desc: str, 
               format:str='%H:%M:%S'):
    try:
        t_second = datetime.strptime(time_desc, format)
        t_second = t_second - datetime(1900, 1, 1)
        t_second = t_second.total_seconds()
        return t_second
    except ValueError:
        return None
    

# ===== LOGGING SYSTEM =====
def set_logger(filename:str='./log/app.log'):
    # Create an empty log file if not exist
    if not os.path.exists(filename):
        os.mkdir(filename)

    # Set logging config
    logging.basicConfig(
                        level=logging.DEBUG,
                        format='[%(asctime)s] - %(levelname)7s --- %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=filename,
                        filemode='w'
                        )
  