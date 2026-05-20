import os #OS is a module used to work with directories, folders and files
import sys
from src.exception import CustomException #We are importing the function which we made in src folder's exception file called CustomException. We know inside this function we could raise exceptions. 
from src.logger import logging #We are importing the function which we made in src folder's logger file called logging. This function helps us to store messages in LOG_FILE in Logs folder. 
from sklearn.model_selection import train_test_split
import pandas as pd
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig: #Now this is DataIngestionConfig. Such configuration is made in all either Data Ingestion file or transformation file or model trainer file. In this configuration we basically tells what will be file path where our files would be stored. Like where will be our train_data file will be stored in whcih folder with which name, same for train_data and raw_data. Because ofcourse we will be storing these files in some place.  This class DataIngestionConfig does not need def __init__. Why? Because we have used a decorator pre defined in Python library called dataclasses which we imported. If we write this decorator before our class we don't need to write def __init__.  Now in this class we just write file_path. We don't do anything else. 
    train_data_path:str=os.path.join("Artifacts", "train.csv") #What will be file_path for our train_data. First of all file_path for our train_data will be in strings, as we can see train_data_path:str means it will be in string. Then, we have to say what will be inside train_data_path. It says it will have train.csv inside Artifatcs folder. Means our training data will be stored in a file called train.csv inside a folder named Artifacts. Currently no such folder exists and no such file exists. We just say train_data_path is train.csv inside Artifacts.  
    test_data_path:str=os.path.join("Artifacts", "test.csv") #Same for test_data_path
    raw_data_path:str=os.path.join("Artifacts", "raw.csv")# and raw data path

class DataIngestion: #Now this is another class we made called DataIngestion. Here, we did not use @dataclass decorator. 
    def __init__(self): # We are initiating this class with just self. 
        self.ingestion_config=DataIngestionConfig() #In self.ingestion_config variable we are calling DataIngestionConfig() class which will give train_data_path, test_data_path and raw_data_path to self.ingestion_config. And we can use self.ingestion_config in same class DataIngestion in other function inside this class. 
    def initiate_data_ingestion(self): # Here we made another function in same  DataIngestion class so we could use self.ingestion_config variable in this function because both this function and self.ingestion_config belongs to same class.
        logging.info("Entered the data ingestion component") # First of all we will store a message in logs folder's LOG_FILE.
        try: # We use try and except so that if any error occurs in try it goes to except and we raise CustomException so that our error becomes clearly visible that what it is.
            df=pd.read_csv('notebook/data/stud.csv') #We first read file notebook/data/stud.csv and uploaded it in df var.
            logging.info("Read The Dataset as CSV") #Stored message

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) # Now as I said previously remember that train_data_path, test_data_path or raw_data_path does not create folder artifacts and inside it train.csv or test.csv etc.. It just says those files inside artifacts folder. Only os.makedirs make folders. So, here we are making folder through os.makedirs and that folder's name os.path.dirname will be self.ingestion_config.train_data_path. So what does self.ingestion_config.train_data_path has? It says train.csv inside Artifacts folder. So, this os.makedirs will make Artifacts folder, because os.makedirs makes only folders.


            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Train-Test split initiated") #df.to_csv will convert our df data to csv file. And where it will go, it will go to this path "self.ingestion_config.raw_data_path" And what does self.ingestion_config.raw_data_path has? It says rawdata.csv inside Artifacts folder. So artifacts folder already exists due to above command but this will make  a csv file named rawdata.csv inside Artifacts folder and store whatever data is in df variable there in csv format. 

            train_set, test_set=train_test_split(df, random_state=42, test_size=0.33)
            #It basically splits our raw data in df var to train and test data and store them in variables

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) #train_set.to_csv will convert our train_set data to csv file. And where it will go, it will go to this path "self.ingestion_config.train_data_path" And what does self.ingestion_config.train_data_path has? It says traindata.csv inside Artifacts folder. So artifacts folder already exists due to above command but this will make  a csv file named rawdata.csv inside Artifacts folder and store whatever data is in train_set variable there in csv format. 

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) # Same like above 2

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            ) # After all of this it returns our self.ingestion_config.train_data_path and self.ingestion_config.test_data_path means path for our train and test data like this /Artifacts/train.csv.


        except Exception as ex: #If try fails go here and here raise Custom Exception so that we could see exactly at what file, at what line was proble and what exactly was our problem. 
            raise CustomException(ex, sys) #Problem is ex found through Exception predefined function.


if __name__==('__main__'):#If we run this file
    obj=DataIngestion()  # Make an object called obj using DataIngestion class
    # obj.initiate_data_ingestion() #This class has function initiate_data_ingestion so call that function, what it will do, it will store train.csv inside artifacts folder, same for test.csv and raw data before making Artifacts folder and storing dtaa in df. 

    train_data, test_data=obj.initiate_data_ingestion() # This class has function initiate_data_ingestion so call that function, what it will do, it will store train.csv inside artifacts folder, same for test.csv. 

    data_transformation=DataTransformation() # We are calling DataTransformation class here and making data_transformation through it
    # data_transformation.initiate_data_transformation(train_data, test_data)
    # We are using a function inside DataTransformation class called initiate_data_transformation which will initiate data transformation on train and test data and return transformed train and test data as well path of preprocessor.pkl file.
    
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data) #This transforms our train_data, test_data and store transformed train_data, and test_data at train_arr, test_arr. 

    model_trainer=ModelTrainer() # Making an object of ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))
    #Initiating model_trainer and printing it to find best r2_score of best_model.

            
    
    
      
    



