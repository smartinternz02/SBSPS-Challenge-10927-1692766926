from flask import Flask,request,render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('classification_gb_sm.pkl', 'rb'))


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
    op = model.predict(input)
    print(op)
    return render_template('input.html',Output=str(op))

if __name__ == '__main__':
    app.run()