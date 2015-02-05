import os
from flask import Flask
from lib.las import jsonifyLAS

app = Flask(__name__)
app.debug = True

@app.route('/')
def root():
  return ''

@app.route('/json/london_analysis_seminar')
def LAS():
  return jsonifyLAS()