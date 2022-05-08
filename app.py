from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open("random_forest_regression_model.pkl","rb"))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def perdict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Fuel_Type = request.form['Fuel_Type']
        if (Fuel_Type=="Petrol"):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif (Fuel_Type=="Diesel"):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        Seller_Type = request.form['Seller_Type']
        if (Seller_Type=="Individual"):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission = request.form['Transmission']
        if (Transmission=="Manual"):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        Owner = int(request.form['Owner'])
        no_years = 2020-Year
        
        Prediction = model.predict([[Present_Price,Kms_Driven,Owner,no_years,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(Prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry, You cannot sell this car")
        else:
            return render_template("index.html", prediction_text = "You can sell this car at {}".format(output))
        
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)
    