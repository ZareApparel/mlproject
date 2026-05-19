import os # os is a built in module in Python which allows us to work with directories, folders and files
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass   # With this pre defined decorator,  class made beneath it will not require def __init__ to use.  
class DataTransformationConfig: #This class is made for basic configuration with respect to path for our preprocessor object. Means, indeed we will create a preprocessor object in this file because this file is about Data Transformation and here we will be transforming our data, by doing encoding of categorical columns, standard scaling, etc.. So for this we can create an object that object has all functionalities of doing all of that. We can create pickle of that object and store it, so we will just call that pickle and it can do data transfromation of any data. So, this class just tells the path where our pickle preprocessor.pkl will be stored.
    preprocessor_obj_file_path=os.path.join("Artifacts", "preprocessor.pkl")
# So here in preprocessor_obj_file_path is a variable made inside ataTransformationConfig. This variable, preprocessor_obj_file_path says preprocessor.pkl inside Artifacts folder. It does not create Artifacts folder or pkl file. It just has path, preprocessor.pkl inside Artifacts folder. 
class DataTransformation: #This is another class, main class where we will be doing transformation
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        #Here, self.data_transformation_config is a variable which now calls previous class DataTransformationConfig(). And when it calls that class, self.data_transformation_config now has preprocessor_obj_file_path means file path for pickle object. It now has path i.e. pkl file inside Artifacts folder. We created this self.data_transformation_config so thatw e could use file path for our pkl object in same class anywhere which we will be using. 
    def get_data_transformer_object(self): # This is a function we created inside same class where we will be creating object for transformation of data. 
        try:
            num_columns=["writing_score", "reading_score"]
            # As we need numerical columns separately for transformation and categorical separately, so we specify that.
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            # Now here we have created pipelines. So what is pipeline. It means a method where we can do multiple steps automatically one after another. 
            num_p=Pipeline( # In this num_p pipeline, first come (then under them steps=[Here are 2 steps, one after other automatically done when we call num_p, in 1st step there is imputer. In imputer we impute values. If there are missing values, we impute them through techniques like median, mode. Like, in numerical data we impute missing values through median, missing values will be filled by median. And in categorical by mode as we cannot take median there. Here, "Imputer" is just name for our step. SimpleImputer(strategy='median') is a function we are calling. We imported its class upward. In 2nd step, we are using StandardScaler().  ])
                steps=[
                    ("Imputer", SimpleImputer(strategy='median')),
                    ("Scaler", StandardScaler())
                ]

            
            )

            cat_p=Pipeline(
                #In cat_p pipeline here are 3 steps. In 1st one imputing missing values with mode, in 2nd onehotencoding categorical columns and in 3rd after first two are done, we do standard scaling 
                steps=[
                    ("Imputer", SimpleImputer(strategy='most_frequent')),
                    ("OneHot", OneHotEncoder()),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            ) 

            logging.info(f"Numerical_Columns: {num_columns}")
            logging.info(f"Categorical_Columns: {categorical_columns}")


            preprocessor=ColumnTransformer(
                #This is THE MOST IMPORTANT PART. Here, we are creating the exact object, preprocessor. What it will do. It will be column transforming executing 2 tasks. In 1st step, apply num_p pipeline at num_columns and naming this object as "Num_Pipeline". In 2nd step we apply cat_p pipeline to categorical_columns and naming it as "Cat_Pipeline".
                [
                    ("Num_Pipeline", num_p, num_columns),
                    ("Cat_Pipeline", cat_p, categorical_columns)
                ]
            )
            return preprocessor #Retuning this preprocessor. When this function, get_data_transformer_object(self) will be called, preprocessor will be result which can apply num_p to numerical columns of train_data and test_data and cat_p to categorical columns of train and test_data.
             
        



        except Exception as ex:
            raise CustomException(ex, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
            # We have made another function and this function will actually start data transformation because previously we just made preprocessor variable but did not initiate transformation. Because, we did not upload data, like train_data or test_data. We know to which columns what type of transformation to be applied, like num_columns we specified. But remember nowwhere we gave data. So we know that preprocessor applies num_p pipeline to num_columns (But those num_columns would be present in train_df and test_df which we will now upload. And what will happen when preprocessor applies num_p pipeline to train_df's num_columns, it will first do imputing of missing values then apply standard scaling, same for cat_columns.  )
            try:
                train_df=pd.read_csv(train_path) #Reading train_data from train_path and storing it in train_df
                test_df=pd.read_csv(test_path) # Same for test_data. 

                logging.info("Read train data path")
                logging.info("Read test data path")

                preprocessor_obj=self.get_data_transformer_object()
                # Now in this preprocessor_obj will be our preprocessor variable which applies num_ pipeline to num_columns of our train_df and test_df and cat_p pipeline to our cat_columns. 

                target="math_score"
                #Target column is this botn in train_df and test_df. Means in each of them we have input columns/indepdendent and one output/dependent. This one is dependent in both of these. In codes beneath this line we specifiy input and output features of our train and test df. 

                input_feature_train_df=train_df.drop(columns=[target])
                output_feature_train_df=train_df[target]

                input_feature_test_df=test_df.drop(columns=[target])
                output_feature_test_df=test_df[target]

                logging.info("Applying preprocessing object on training and testinf data")

                input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df) #Here now we are applying preprocessor object on our input features of both train and test data. What will that object do? It will basically apply num_p pipeline to num_columns of our both input features of train and test data. In that num_ p pipeline it will first imput nan values of our input numerical features with median of each column values. Then, it will apply standard scaling. In categorical columns, it will first impute nan values with mode of column then do onehot encoding then it will apply scaling. This is what preprocessor_obj do (preprocessor_obj.fit_transform). And that transformed data will be stored in input_feature_train_arr and input_feature_test_arr.

                input_feature_test_arr=preprocessor_obj.fit_transform(input_feature_test_df) #See above



                train_arr= np.c_[
                    input_feature_train_arr, np.array(output_feature_train_df)
                ]  #Here, in train_arr we will combine both input features transformed with our output feature of train data. np.c_ comhine these two and store result in train_arr.
 
                test_arr= np.c_[
                    input_feature_test_arr, np.array(output_feature_test_df)
                ] #Here, in test_arr we will combine both input features transformed with our output feature of test data. np.c_ comhine these two and store result in test_arr.

                logging.info("Saved Object")

                save_object(
                    file_path=self.data_transformation_config.preprocessor_obj_file_path,
                    obj=preprocessor_obj
                ) #Now this is EXTREMELY important. As we know what we did was that we created an object called preprocessor_obj. But we also have to save that object as a pickle file. So that we can use it anywhere in our project. We will create a function for this (NOT HERE BUT IN UTILS). So that we can call that function anywhere. This function will demand two parameters, one file_path where our preprocessor.pkl object will be stored and other that object itself. Now here we have given both. File Path is self.data_transformation_config.preprocessor_obj_file_path, and we know what it contains, it says preprocessor.pkl in Artifacts folder. 

                return (

                    train_arr, 
                    test_arr,
                    self.data_transformation_config.preprocessor_obj_file_path

                ) #Now when we will call this function, initiate_data_transformation(self, train_path, test_path) and give our train_data, test_data paths this will apply transformation using preprocessor.pkl and return train_arr, test_arr, transformed data and object file path where our pickle object is stored. 
            
            except Exception as e:
                raise CustomException(e, sys)
                
    