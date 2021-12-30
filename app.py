from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    Fuel_Type_CNG=0
    Seller_Type_Dealer=0
    Transmission_Automatic=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])        
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_CNG=0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
                Fuel_Type_CNG=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CNG=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Dealer=0
        else:
            Seller_Type_Individual=0
            Seller_Type_Dealer=1	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
            Transmission_Automatic=0
        else:
            Transmission_Mannual=0
            Transmission_Automatic=1
        
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_CNG,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Dealer,Seller_Type_Individual,Transmission_Automatic,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

@app.route("/carpredict", methods=['POST'])
def carpredict():
    Fuel_Type_Diesel=0
    Fuel_Type_CNG=0
    Seller_Type_Dealer=0
    Transmission_Automatic=0
    if request.method == 'POST':
        car = request.get_json()
        Year = int(car['Year'])
        Present_Price=float(car['Present_Price'])
        Kms_Driven=int(car['Kms_Driven'])        
        Owner=int(car['Owner'])
        Fuel_Type_Petrol=car['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_CNG=0
        elif(Fuel_Type_Petrol=='Diesel'):
                Fuel_Type_Petrol=0
                Fuel_Type_Diesel=1
                Fuel_Type_CNG=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_CNG=1
        Year=2020-Year
        Seller_Type_Individual=car['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Dealer=0
        else:
            Seller_Type_Individual=0
            Seller_Type_Dealer=1	
        Transmission_Mannual=car['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
            Transmission_Automatic=0
        else:
            Transmission_Mannual=0
            Transmission_Automatic=1
        
        prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_CNG,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Dealer,Seller_Type_Individual,Transmission_Automatic,Transmission_Mannual]])
        result = {
            'car_prediction': list(prediction)
        }
        return jsonify(result)
    else:
        return 0

if __name__=="__main__":
    app.run(debug=True)

