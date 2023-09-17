from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from keras.models import load_model
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if __name__ == '__main__':
    app.run (debug=True)

# Partie SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'database/chinook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)



#séance 1 td1

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

#séance 2 td3

@app.route('/uploader', methods = ['POST'])
def upload_image_file():
    if request.method == 'POST':
        img = Image.open(request.files['file'].stream).convert("L")
        img = img.resize((28,28))
        im2arr = np.array(img)
        im2arr = im2arr.reshape(1,28,28,1)
        model = load_model('MNIST_keras_CNN.h5')

        predict_x = model.predict(im2arr)
        y_pred = np.argmax(predict_x,axis=1)
        
        output = 'Predicted Number: ' + str(y_pred[0])
        
        return render_template('td3.html', output=output, predict_x=predict_x, y_pred=y_pred)

#Routes

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/calcul")
def calcul():
    return render_template('calcul.html')

 
@app.route("/td3")
def td3():
    return render_template('td3.html')

 
    