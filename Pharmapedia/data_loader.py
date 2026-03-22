import json
import os
from config import DATA_PATH

def load_json():
    file_path=DATA_PATH
    if os.path.exists(file_path):
        try:
            with open(file_path,mode='r') as file:
                data=json.load(file)
                return data
        except Exception as e:
            print(e)
    else:
        print("path doesn't exists")                    
