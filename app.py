#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:37:59 2023

@author: Tejal
"""

import numpy as np

from flask import Flask, render_template, request
import jsonify
import requests
import pickle

import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__, static_folder='static')
model = pickle.load(open('model/regression_rf_model_v1.pkl', 'rb'))
standard_to = StandardScaler()
scaler = pickle.load(open('model/scalar_v1.pkl','rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        
        Year = int(request.form['Year'])
        Year=2020-Year
       
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=float(request.form['Kms_Driven'])
        
        inputs = [[Year, Present_Price, Kms_Driven]]
        normalized_inputs = scaler.transform(inputs)
        
        Year2 = normalized_inputs[0][0]
        Present_Price2 = normalized_inputs[0][1]
        Kms_Driven2 = normalized_inputs[0][2]
        
        Owner=int(request.form['Owner'])
        
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else :
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            
        
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
            
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
            
        prediction=model.predict([[Present_Price2,Kms_Driven2,Owner,Year2,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry! Unfortunately you cannot sell this car.")
        else:
            return render_template('index.html',prediction_text="You can sell this car at {} lakh (INR)".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)