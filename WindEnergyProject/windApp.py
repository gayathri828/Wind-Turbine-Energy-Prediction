from flask import Flask, render_template, request
import joblib
import requests

app = Flask(__name__)
model = joblib.load("power_prediction.sav")

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get("city")

    apikey="aa216216ed717b2347ecafdbfe2b7c02"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey

    resp=requests.get(url).json()

    temp=str(resp["main"]["temp"])
    humid=str(resp["main"]["humidity"])
    pressure=str(resp["main"]["pressure"])
    speed=str(resp["wind"]["speed"])

    return render_template('predict.html',
                           temp=temp,
                           humid=humid,
                           pressure=pressure,
                           speed=speed)

@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test=[[float(x) for x in request.form.values()]]
    prediction=model.predict(x_test)
    output=prediction[0]

    return render_template('predict.html',
    prediction_text='The energy predicted is {:.2f} KWh'.format(output))

if __name__=="__main__":
    app.run(debug=True)
