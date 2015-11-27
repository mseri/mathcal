from flask import Flask, request
from scrapers import gcal, custom

app = Flask(__name__)
app.debug = False


@app.route('/')
def root():
    return "The service is active! For the calendar visit <a href='http://www.mseri.me/mathcal'>www.mseri.me/mathcal</a>"


@app.route('/json/gcal/<gcal_id>')
def GCAL(gcal_id):
    return gcal(gcal_id)


@app.route('/json/<path:path>')
def catch_all(path):
    return custom(path)


# try to solve No 'Access-Control-Allow-Origin' error
# http://mortoray.com/2014/04/09/allowing-unlimited-access-with-cors/
@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
          by the client. """

    resp.headers['Access-Control-Allow-Origin'
    ] = request.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, GET'

    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'

    return resp


if __name__ == '__main__':
    app.run()

# This app really needs to be refactored, 
# it's fairly easy but I have no time for it at the moment
