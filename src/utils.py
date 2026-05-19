import os #Importing Os module a built in module in Python used to handle directories/folders, files, etc...
import sys

import numpy as np
import pandas as pd
import dill

from src.exception import CustomException 

def save_object(file_path, obj): #Now here in Utils we are creating a function to save object in folder. This will have 2 paramaters, one we wil give file_path where we want our object to be saved and other obj itself. 
    try:
        dir_path=os.path.dirname(file_path) #It means what will be our file_path where will be our folder made and what will be name of our folder. os.path.dirname means what will be name of our directory. And where will it be made, like in os.getcwd() current directoy. It will extract only folder path and store in dir_path not file. 
        os.makedirs(dir_path, exist_ok=True) #This is what actually creates that folder or if that already exists don't create new. os.makedirs

        with open(file_path, 'wb') as w: #Now here with open(file_path, 'wb) means open file_path, suppose if file_path as Artifacts/preprocessor.pkl (Suppose), then it opens preprocessor.pkl but if preprocessor.pkl does not exist it creates one as we used 'wb' mode where w stands for write like make new file if not exist. And then that file is now 'w'. 
            dill.dump(obj, w) #Now here we are storing our object into that file and taht file will become our pickle file, and can be used for data transformation or something else for which we created our object. dill.dump requires our object and file where object is to be stored.
    except Exception as e:
        raise CustomException(e, sys)
    