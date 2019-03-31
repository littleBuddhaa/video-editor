import os
from flask import Flask, render_template,flash, request, redirect, url_for, session, request,logging
import urllib.request
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.config import get_setting
import datetime

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
session_url = ''

@app.route('/')
def index():
    subprocess.run(['rm' , 'static/cropped/new.webm'])
    subprocess.run(['rm' , 'static/uploads/mysample.webm'])


    return render_template('home.html')

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        url = (request.form['url'])
        print ('Downloading Started..')
        up = 0
        name  = 'static/uploads/mysample.webm'
        session_url = name
        urllib.request.urlretrieve(url, name)
        print ('Download Completed!')
        up = 1
        dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', name])
        print (dur)
        
    return render_template('home.html',var = up,url = url,dur = str(dur))
@app.route('/crop',methods = ['GET','POST'])
def crop():
    if request.method == 'POST':
        start = (request.form['start'])
        end  = (request.form['end'])
        print ('user entered from (%f) to (%f)',(start,end))
        hrst = (datetime.timedelta(seconds=int(start)))
        hrend = (datetime.timedelta(seconds=int(end)))
        crurl = '../static/cropped/new.webm'
        try:
            print('******************************')
            print(session_url)
            #subprocess.run(['ffmpeg_extract_subclip(', session_url ,',', start,',', end,',', 'targetname="/downloads/cropped.webm")'])
            #subprocess.run(['ffmpeg_extract_subclip( session_url, start, end, targetname="/downloads/cropped.webm")'])
            #subprocess.run(['ffmpeg', '-i' , 'uploads/mysample.webm', '-ss' ,  str(hrst), '-to' , str(hrend), '-c:v' ,  'copy' , '-c:a' , 'copy' ,  'cropped/new.webm'])
            subprocess.run(['ffmpeg', '-i' , 'static/uploads/mysample.webm', '-ss' ,  str(hrst), '-to' , str(hrend), 'static/cropped/new.webm'])

            err = 0
        except subprocess.CalledProcessError as e:
            print (e.output)
            err = 1


    return render_template('home.html',err = err,crurl = crurl)

    

if __name__ == '__main__':
    app.secret_key = 'sec123'   
    app.run(debug=True)