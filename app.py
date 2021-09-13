# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 16:57:20 2021

@author: Hasan Mahamud Rana

"""

from flask import Flask, render_template, request, send_from_directory
from system__database import dbClass
from system__send_email import emailClass
from system__send_sms import smsClass
from source__craig import craiglstClass
from source__kijiji import kijijiClass
import pandas as p
import os

app = Flask(__name__, static_folder = os.path.abspath('assets'))

@app.route('/')

# defination of landing page
def index():
  return render_template('index.html')

# Set route for result page with method post
@app.route('/result', methods=['POST'])

# defination of result page
def result():

  # Condition to check request method type
  if request.method == 'POST':

    # On success Store data using DB class
    d = dbClass(request.form)
    d.storeData()

    # On success Send email using email class
    e = emailClass(request.form)
    e.emailSend()

    # On success Send SMS using sms class
    s = smsClass(request.form)
    s.smsSend()
 
    # print(request.form)

    # Declare object
    obj = []

    # Check source Kijiji is checked or not
    if (request.form['s-source[0]']  == '1'):
      # Call kijiji Class
      k = kijijiClass(request.form)
      # get object from kijiji Class getListing methods and add it to obj 
      obj += k.getListing()

    # Check source craig list is checked or not
    if (request.form['s-source[1]']  == '1'):
      # Call craig list Class
      c = craiglstClass(request.form)
      # get object from craig list Class getListing methods and add it to obj 
      obj += c.getListing()
    
    # print('Object', obj)
    # Create dataframe using panda
    df = p.DataFrame(obj)
    # Create/Save dataframe to result csv
    df.to_csv('output/result.csv')

    return render_template('result.html')

if __name__ == '__main__':
  app.debug = True
  # initilize flask ap
  app.run()