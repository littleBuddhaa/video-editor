import os
from flask import Flask, render_template,flash, request, redirect, url_for, session, request,logging
import urllib.request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():


    return render_template('home.html')

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        url = (request.form['url'])
        print ('Downloading Started..')
        name  = 'mysample.webm'
        urllib.request.urlretrieve(url, name)
        print ('Download Completed!')
        
    return redirect(url_for('index'))

    

if __name__ == '__main__':
    app.secret_key = 'sec123'   
    app.run(debug=True)