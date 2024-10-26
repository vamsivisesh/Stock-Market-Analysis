from flask import Flask, render_template,request,redirect,url_for
import pred
import io
import os
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import glob
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/report/<button_id>')
def report(button_id):
    if not os.path.exists('static/images/'+button_id):
      os.makedirs('static/images/'+button_id)
      pred.report(button_id)
      f = open("static/images/"+button_id+"/time.txt", "w")
      f.write(datetime.now().strftime("%Y-%m-%d"))
      f = open("static/images/"+button_id+"/low_date.txt", "r")
      low_date = datetime.strptime(f.read()[:10], '%Y-%m-%d')
      f = open("static/images/"+button_id+"/high_date.txt", "r")
      high_date = datetime.strptime(f.read()[:10], '%Y-%m-%d')
      f.close()
      print("folder created")
      return render_template('result.html',comp=button_id,low_date=low_date,high_date=high_date)
    else:
     f = open("static/images/"+button_id+"/time.txt", "r")
     date_object = datetime.strptime(f.read(), '%Y-%m-%d')
     f = open("static/images/"+button_id+"/low_date.txt", "r")
     low_date = datetime.strptime(f.read()[:10], '%Y-%m-%d')
     f = open("static/images/"+button_id+"/high_date.txt", "r")
     high_date = datetime.strptime(f.read()[:10], '%Y-%m-%d')
     f.close()
     if date_object.date()<datetime.now().date():
        try:
          files = glob.glob('static/images/'+button_id+'/*')
          for f in files:
           os.remove(f)
          pred.report(button_id)
          f = open("static/images/"+button_id+"/time.txt", "w")
          f.write(datetime.now().strftime("%Y-%m-%d"))
          f.close()
        except Exception as e:
          print('Reason: %s' % (e))
        print("data reload needed")
        return render_template('result.html',comp=button_id,low_date=low_date,high_date=high_date)
     else:
      print("not needed")
      return render_template('result.html',comp=button_id,low_date=low_date,high_date=high_date)
    
if __name__=='__main__':
    app.run(debug=True)
    app.run()