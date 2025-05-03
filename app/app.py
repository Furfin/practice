import random

from concurrent.futures import thread
from fileinput import filename
from flask_sqlalchemy import SQLAlchemy
import main
from flask import Flask,render_template,redirect,request, Response, url_for
import os
app = Flask(__name__)
results = {}

@app.route('/video/<filename>')
def video(filename):
    global results
    filepath = os.path.join(app.static_folder, filename)
    file_exists = os.path.exists(filepath)
    
    if not file_exists:
        return f"Video {filename} not found in static folder", 404
    return render_template("index.html",filename = filename, count = results[filename])

@app.route('/')
def index():
   return render_template('upload.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   global results
   if request.method == 'POST':
      f = request.files['file']
      if f.filename.split(sep='.')[1] != "mp4":
          return "Invalid file extension! Try again"
      f.save("static/"+str(f.filename))
      filename,count = main.track('static/' + str(f.filename))
      results[filename] = count
      return  redirect('/video/' + filename)

if __name__ == '__main__':
   app.run(debug = True)