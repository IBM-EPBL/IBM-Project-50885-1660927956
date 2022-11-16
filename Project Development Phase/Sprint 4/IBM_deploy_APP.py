import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Tom599kqOh5z7-ESosmDFH2LVlj_OIi89qU-d9G36ZEQ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#model = pickle.load(open("university.pkl", "rb"))

@app.route("/")
def home():
    return render_template('Demo2.html')

@app.route("/y_predict", methods = ["POST","GET"])
def y_predict():
    gre = request.form["t1"]
    toefl = request.form["t2"]
    rating = request.form["University Rating"]
    sop = request.form["t3"]
    lor = request.form["t4"]
    cgpa = request.form["t5"]
    research = request.form["Reserch"]

    if (research == "0"):
         research = 0
    if (research == "1"):
         research = 1
    #min1 = [290.0, 92.0, 1.0, 1.0, 1.0, 6.8, 1]
    #max1 = [340.0, 120.0, 5.0, 5.0, 5.0, 9.92, 2]
    #k = [float(x) for x in request.form.values()]
    #print(k)
    #p = []
    #for i in range(7):
     #   l = (k[i]-min1[i])/(max1[i]-min1[i])
      #  p.append(l)
    t = [[int(gre), int(toefl), float(rating), float(sop), float(lor), float(cgpa), int(research)]]
    print(t)
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]], "values":t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/58094de1-d45c-4339-a236-4607aef64478/predictions?version=2022-11-16',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    pred = response_scoring
    print(pred)
    p= pred.json()
    output= p['predictions'][0]['values'][0][0]

    if output== True:
        return render_template("chance.html", prediction_text="you have a chance")
    else:
        return render_template("noChance.html", prediction_text="you dont have a chance")


if __name__ == "__main__":
    app.run(debug=True)