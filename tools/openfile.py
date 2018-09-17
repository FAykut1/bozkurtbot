import json
import os

def Open(filename:str):
    try:
        with open(filename,'r') as fp:
            files = json.load(fp)
            return files
    except FileNotFoundError:
        return None