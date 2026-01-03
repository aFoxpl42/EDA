import os
import pandas as pd

def analyze_csv(filepath:str):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            df = pd.read_csv(filepath, delimiter=';')
            return df.shape[0], df.shape[1], df.head(), df.isna().sum()
    else: 
        print(f"File: {filepath} doesn't exist!")
        os._exit(1)
