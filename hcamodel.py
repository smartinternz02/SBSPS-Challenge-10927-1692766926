# Step 1 - Importing the required lib

from flask import Flask,request,render_template
import pickle

# Step 2 - Initializing the flask

app = Flask(__name__)
model = pickle.load(open('classification_gb_sm.pkl', 'rb'))

# Step 3 - Routing to the templates with some functionalities
@app.route('/')
def home():
    return render_template('input.html')


@app.route('/input',methods = ['POST'])
def pred():
    gender = request.form.get('gender')
    ssc_b = request.form.get('ssc_b')
    hsc_b = request.form.get('hsc_b')
    degree_t = request.form.get('degree_t')
    workex = request.form.get('workex')
    specialisation = request.form.get('specialisation')
    status = request.form.get('status')
    hsc_s_Arts = request.form.get('hsc_s_Arts')
    hsc_s_Commerce = request.form.get('hsc_s_Commerce')
    hsc_s_Science = request.form.get('hsc_s_Science')
    input = [[int(gender), int(ssc_b), int(hsc_b), int(degree_t),int(workex), int(specialisation), int(status), int(hsc_s_Arts), int(hsc_s_Commerce), int(hsc_s_Science)]]
    import requests

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "u3NGWPGvt98WfwbStWuqtaTdI-4GdYieODsBdz9vo3Yr"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Gender", "ssc_b", "hsc_b", "degree_t", "workex", "spcialisation" ,"status", "hsc_s_Arts", "hsc_s_Commerce", "hsc_s_Science"],
                                       "values": [[int(gender), int(ssc_b), int(hsc_b), int(degree_t),int(workex), int(specialisation), int(status), int(hsc_s_Arts), int(hsc_s_Commerce), int(hsc_s_Science)]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/1bf8f596-e9a4-4519-823a-2ca2c2ba50d3/predictions?version=2021-05-01',json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    op = response_scoring.json()
    print(op)
    return render_template('input.html',Output=str(op))


# Step 4 - Run the application

if __name__ == '__main__':
    app.run()