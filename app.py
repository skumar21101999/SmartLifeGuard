import flask
import pickle
import pandas as pd

with open(f'model/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='templates')
# app.static_folder = 'static'

@app.route('/')
def hello_world():
    return( flask.render_template("Drowning.html"))

@app.route('/predict', methods=['GET', 'POST'])

def predict():
    # if flask.request.method == 'GET':
    #     return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        heartbeat = int(flask.request.form['heartbeat'])
        systolicbp = int(flask.request.form['systolicbp'])
        diastolicbp = int(flask.request.form['diastolicbp'])
        spo2 = int(flask.request.form['spo2'])
        input_variables = pd.DataFrame([[heartbeat, systolicbp, diastolicbp, spo2]])
        prediction = model.predict(input_variables)[0]
        if heartbeat<60 or heartbeat>110 or systolicbp <75 or systolicbp >130 or diastolicbp<55 or diastolicbp>85 or spo2<85 or spo2>101:
            return flask.render_template('Drowning.html',result='\nErr:Values should be in a consised range....')
        else:
            if prediction <= 3:
                return flask.render_template('Drowning.html',result='\nPerson Not Drowning.... ')
            else:
                return flask.render_template('Drowning.html',result='\nProbability of person drowning is HIGH (Blinking on screen....) ')
if __name__ == '__main__':
    app.run()