import os
from flask import Flask, request
from lib.las import jsonifyLAS
from lib.nts import jsonifyNTS
from lib.imp import jsonifySAS, jsonifyTAKTIC ,jsonifyAPDE, jsonifyAMMP, jsonifyFD, jsonifyFTMP
from lib.impprob import jsonifyIP
from lib.impgeom import jsonifyIPGAS, jsonifyIPLTGS

app = Flask(__name__)
#app.debug = True

@app.route('/')
def root():
  return "The service is active! For the calendar visit <a href='http://www.mseri.me/mathcal'>www.mseri.me/mathcal</a>"

@app.route('/json/las')
def LAS():
  return jsonifyLAS().cache

@app.route('/json/nts')
def NTS():
  return jsonifyNTS().cache

@app.route('/json/ic/sas')
def SAS():
    return jsonifySAS().cache

@app.route('/json/ic/taktic')
def TAKTIC():
    return jsonifyTAKTIC().cache

@app.route('/json/ic/apde')
def APDE():
    return jsonifyAPDE().cache

@app.route('/json/ic/ammp')
def AMMP():
    return jsonifyAMMP().cache

@app.route('/json/ic/fd')
def FD():
    return jsonifyFD().cache

@app.route('/json/ic/ftmp')
def FTMP():
    return jsonifyFTMP().cache

@app.route('/json/ic/ip')
def IP():
    return jsonifyIP().cache

@app.route('/json/ic/ipgas')
def IPGAS():
    return jsonifyIPGAS().cache

@app.route('/json/ic/ipltgs')
def IPLTGS():
    return jsonifyIPLTGS().cache


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

if __name__ == '__main__':
    app.run()
