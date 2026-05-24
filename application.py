from flask import Flask, request, render_template
# Importing Flask to make our app, also request to check request and to receive values from html page, and also importing render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, predict_pipeline

application=Flask(__name__) #Making Flask application using name application

app=application #Using name app instead of application 

@app.route('/')
def index():
  return "Welcome To Home Page"

@app.route('/predictdata', methods=['GET', 'POST'])
# Here, when we will use url /predictdata, what will happen is that it will check if request.method=='GET', means are we sending request to server to see the page. If yes, we will be sent to home.html through render_template.
def predict():
  if request.method=='GET':
    return render_template('home.html')
  else:
    data=CustomData(
      gender=request.form.get('gender'),
      race_ethnicity=request.form.get('ethnicity'),
      parental_level_of_education=request.form.get('parental_level_of_education'),
      lunch=request.form.get('lunch'),
      test_preparation_course=request.form.get('test_preparation_course'),
      reading_score=float(request.form.get('writing_score')),
      writing_score=float(request.form.get('reading_score'))
    )
    pred_df=data.get_data_as_data_frame()
    print(pred_df)

    predict=predict_pipeline()
    results=predict.predict(pred_df)

    return render_template('home.html', results=results[0])
  
if __name__=="__main__":
    app.run(host='0.0.0.0')

