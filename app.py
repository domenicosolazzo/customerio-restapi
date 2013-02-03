import os
import uuid
from customerio import CustomerIO
from flask import Flask, jsonify, json
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException, NotFound
from dbFacade import DBFacade

siteKey = os.environ.get('siteKey', None)
appKey = os.environ.get('apiKey', None)

def json_flask_app(import_name, **kwargs):
    def make_json_error(ex):
        response = jsonify(message=str(ex), code=ex.code if isinstance(ex, HTTPException) else 500)
        return response
    app = Flask(import_name, **kwargs)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    return app

facade = DBFacade().getInstance('customerio.db', 'sqlite')
app = json_flask_app(__name__)


cio = CustomerIO(siteKey, appKey)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/signup/<email>')
def signupCustomer(email):
    check = facade.retrieveEmail(email)
    if len(check) > 0:
        # Take the first result
        customer = check[0]
        return jsonify(data=[{
            'id':customer[0],
            'email':customer[1]
        }])
    else:
        facade.saveEmail(email)
        result = facade.retrieveEmail(email)
        resultDict = [{'id':item[0], 'email':item[1]} for item in result]
    return jsonify(data=resultDict)

@app.route('/customers/<email>/events/<eventname>')
def sendEvent(email, eventname):
    return jsonify(data={
        'email': email,
        'event': eventname
    })

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

