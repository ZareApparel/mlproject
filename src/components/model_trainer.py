import os # Importing OS module used for handling directories, files, etc..
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import  LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import  DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.utils import save_object, evaluate_models
from src.logger import logging

@dataclass #By using this decorator, we don't need to write def __init__ beneath the class made beneath this decorator.
class ModelTrainerConfig: #This class is used for configuration for our file, here we decide what will be path for our model.pkl, like when we will store our model in pickle file what will be its path
    trained_model_file_path= os.path.join('Artifacts', 'model.pkl')
    # here we made a variable called, trained_model_file_path where we will store file path for our model which would have been trained, and we use os.path.join for that, and give our folder as "Artifacts", and file as "model.pkl" where we will store our model. As we used linux mini system in setup.py to run this project, now if we just use Artifacts/model.pkl it will cause trouble because both linux and windows have different ways to access file some use /, some \. SO we use os.path.join for safety. 

class ModelTrainer:
    #This is actual class where we will be training our models and finding best model and storing it in pkl file in Artifacts folder. 
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
        # We store the file path previously stored in trained_model_file_path in class ModelTrainerConfig to self.model_trainer_config. Now, self.model_trainer_config has file path for where our model will be stored. And we stored it in self.model_trainer_config so that we can use it in other functions belonging to same class, as self.model_trainer_config also belongs to class ModelTrainer and the function where we will storing it in pkl form will also be belonging to same class.
    def initiate_model_trainer(self, train_arr, test_arr):
        # This function will initiate model training process where we will be actually training our model. 
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test=[ # Here we are spliting our data from train_arr and test_arr to X_train, y_train, X_test, y_test.
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
                
            ]

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(verbose=False),
                "AdaBoost Classifier": AdaBoostRegressor(),
}
            
            


            params={ #These are our parameters. Trying with different parameters and choosing best ones improve accuracy of our model. Here, in params dictionary name of each model is given then its parameters. 
                
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "K-Neighbour Regressor":{
                    'n_neighbors': [5,7,9,11],
                    # 'weights':['uniform','distance'],
                    # 'algorithm':['ball_tree','kd_tree','brute']
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
}
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models, param=params) #Here we are making a variable called model_report in dictionary form and in that model_report we will call function evaluate_models which is in utils and we initially imported it. evaluate_models will require, X_train, y_train, X_test, y_test and models dictionary which will have all of our models in models dictioary. For example, "Random Forest": RandomForestRegressor(), "Decision Tree": DecisionTreeRegressor(), etc.... Now, result of evaluate_models will be stored in model_report. Result of evaluate_models would be like, "Random Forest": some numerical value as r2 score of this specific model, same for every other model. Evaluate Models function will use predicted output of that model on testing data and y_test for finding r2 score and from all models' r2 score we will see which model has best r2 score and that model's name (Found through model_report keys ) as keys = name, and value= r2 score. We will use that model as our best model.

            best_model_score=max(sorted(model_report.values()))
            #First we will get result of model_report as model1: r2_score1, model2: r2_score2, model3: r2_score3, etc.. where in model1, model2, model3, etc... there would be names of models, like RandomBoost, etc.. and in model_report.keys, like r2score1, etc.. there would be there r2 scores. So best_model_score will do what it will first model_report_values() means r2_score1, r2score2, etc.. then it will find max value among them and store them in best_model_score. 

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ] #Here as we have found best_model_score, we will find best_model_name. As we know that model_report.keys() contain names of models, like  model1, model2, model3, etc... there would be names of models, like RandomBoost, etc... So it will check which model name (model_report.keys()) has highest r2score(model_report.values()) and return name of that specific model. We know when we write model_report.keys()[1], it will will find which model is in index 1. Here what we did we instead of writing [1] or [i] we wrote code to find index of best r2_score, through this list(model_report.values()).index(best_model_score. It is what we wrote in [], We made a list of model_report's r2_scores here, list(model_report.values()) then then found where in which index best_model_score lies, then this code would give index like 1, 2,3,4,5, etc.. Then in outer part, list(model_report.keys()) will make list of model_report.keys(), means list of names of models, then through [i] it will find that specific model name in that specific index then we will store that name of best model which has highest r2_score in best_model_name.


            best_model=models[best_model_name]

            if best_model_score<0.6:
                #If the best_model_score is less than 0.6 we will say best model not found in error we will raise custom deliberate error for this, because 0.6 means 60% is already not a good score. 
                raise CustomException("No Best Model Found")
            logging.info("Best model found")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            #We will call save_object function and give our file path and obj name as parameters. It will save our obj in Artifacts folder as model.pkl. Why? Because file-_path is given as self.model_trainer_config.trained_model_file_path. Object is given as best_model. What best_model does? It find best_model_name in models dictionary, and best_model_name is found through using best_model_score. So this model will be stored in model.pkl file in Artifacts folder. When we will have models dictionary it can find best model from it.

            pred=best_model.predict(X_test) #We will predict output values through our best_model_score and see score.
            r2_s=r2_score(y_test, pred)
            return r2_s


            
        except Exception as e:
            raise CustomException(e, sys)

    
