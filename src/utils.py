import os #Importing Os module a built in module in Python used to handle directories/folders, files, etc...
import sys

import numpy as np
import pandas as pd
import dill

from src.exception import CustomException 
from sklearn.metrics import r2_score

def save_object(file_path, obj): #Now here in Utils we are creating a function to save object in folder. This will have 2 paramaters, one we wil give file_path where we want our object to be saved and other obj itself. 
    try:
        dir_path=os.path.dirname(file_path) #It means what will be our file_path where will be our folder made and what will be name of our folder. os.path.dirname means what will be name of our directory. And where will it be made, like in os.getcwd() current directoy. It will extract only folder path and store in dir_path not file. 
        os.makedirs(dir_path, exist_ok=True) #This is what actually creates that folder or if that already exists don't create new. os.makedirs

        with open(file_path, 'wb') as w: #Now here with open(file_path, 'wb) means open file_path, suppose if file_path as Artifacts/preprocessor.pkl (Suppose), then it opens preprocessor.pkl but if preprocessor.pkl does not exist it creates one as we used 'wb' mode where w stands for write like make new file if not exist. And then that file is now 'w'. 
            dill.dump(obj, w) #Now here we are storing our object into that file and taht file will become our pickle file, and can be used for data transformation or something else for which we created our object. dill.dump requires our object and file where object is to be stored.
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models):
        #This is a model we made called evaluate_models, here we take X_train, y_train, X_test, y_test, models and return r2_score of each model. Here, models is a dictionary containing model names.
        try:
            report={} # Making an empty dictionary
            for i in range(len(list(models))): # Means for i in range(length of total number of models in models dictionary, like if there are 10 models so iteration will happen 10, for first time i will be 1, for 2nd time i will be 2, for 3rd time it will be 3 and so on)
                model=list(models.values())[i]  #If i=1 means for model at 1st index, store it in model. We know models dictionary has 2 parts in our case at model_trainer, one model.keys() which have names of models, like "Random Forest", "Decision Tree", etc.. One model.values() which have RandomForestRegressor(), DecisionTreeRegressor() means calling the models which we imported upwards. So in (models.values())[1] means model.values() at 1st index be stored at model variable. 

                model.fit(X_train, y_train) #Now do model.fit at X_train and y_train, means DecisionTreeRegressor().fit(X_train, y_train)

                p_train=model.predict(X_train) #Predict y of training data set

                p_test=model.predict(X_test) #Predict y of testing data set

                train_model_score=r2_score(y_train, p_train) #Scores of train

                test_model_score=r2_score(y_test, p_test) # Of test

                report[list(models.keys())[i]] = test_model_score  #Remember we made a report dictionary upwards an empty one. Here, models.keys())[i] means at that specific i index pick the name of the model and check its test_model_score and store it in report dictionary. It will repeat at le(list(models.values())) times.

                return report # Report will be retuned with test r2 scores of all models. 
            
        except Exception as e:
            raise CustomException(e, sys)
    