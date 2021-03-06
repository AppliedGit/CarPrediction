import requests
import pickle
import numpy as np
import sklearn
import jwt 
import datetime
import uuid
import hashlib
from flask import Flask, render_template, request, make_response, jsonify
from sklearn.preprocessing import StandardScaler
from functools import wraps


app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except Exception as e:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/gettoken')
def gettoken():  
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        
    uname_hash = 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec'      
    password_hash = '263d198e179108ea11ade755d21829b31eb6744f888c77b4bf704472eb70020eed618bbf2b43883484356a2a315b98f622bcdefdafc465e7aaba1a12cef2b0f6'       
    auth_pwd = auth.password.encode('utf-8')
    auth_password_hash = hashlib.sha512(auth_pwd).hexdigest() 
    auth_uname = auth.username.encode('utf-8')
    auth_uname_hash = hashlib.sha512(auth_uname).hexdigest()
       
    if auth and auth_uname_hash == uname_hash and auth_password_hash == password_hash:  
       app.config['SECRET_KEY'] = str(uuid.uuid4().hex)
       unique_id = str(uuid.uuid4().hex)
       token = jwt.encode({'user' : unique_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
       return jsonify({"token" : token.decode("utf-8")})

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


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
        if(Transmission_Mannual=='Manual'):
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
@token_required
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
        if(Transmission_Mannual=='Manual'):
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
