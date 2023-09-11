from flask import Flask, render_template,request
import random

app = Flask(__name__)

@app.route("/test/", methods=['POST'])
def test(): 
    # Your Python function code here 
    
    c1=13.1267
    c2=0.6215
    c3=-0.3965
    
    
    T = int(request.form.get('T'))
    V = int(request.form.get('V'))
    H = int(request.form.get('H'))
    
    print(T)
    print(type(T))
    
    Tressentie = c1 * T - c2 * pow(V, 1/2) + c3 * (T - 91.4 ) * (0.0203 * H) - 0.474
    
    print('hello')
    # var = random.randint(0, 9)

    return render_template('calcul.html', result=Tressentie)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/calcul")
def calcul():
    return render_template('calcul.html')

 
    