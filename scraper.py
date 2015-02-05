import os
from flask import Flask, request
from lib.las import jsonifyLAS

app = Flask(__name__)
# app.debug = True

@app.route('/')
def root():
  return ''

@app.route('/json/london_analysis_seminar')
def LAS():
  return jsonifyLAS().cache

# try to solve No 'Access-Control-Allow-Origin' error
# http://mortoray.com/2014/04/09/allowing-unlimited-access-with-cors/
@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'

    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp