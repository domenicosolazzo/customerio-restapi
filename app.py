import os
import uuid
from customerio import CustomerIO
from flask import Flask, jsonify, json
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException, NotFound
from dbFacade import DBFacade

siteKey = os.environ.get('siteKey', None)
apiKey = os.environ.get('apiKey', None)

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


cio = CustomerIO(siteKey, apiKey)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/signup/<email>', methods=['GET'])
def signupCustomer(email):
    check = facade.retrieveEmail(email)
    if len(check) > 0:
        # Take the first result
        customer = check[0]
        return jsonify(data={
            'customer':{
                'id':customer[0],
                'email':customer[1]
            },
            'signup':False
        })
    else:
        facade.saveEmail(email)
        result = facade.retrieveEmail(email)
        customer = result[0]

        cio.identify(id=customer[0], email=customer[1], signup=1)
        return jsonify(data={
            'customer':{
                'id':customer[0],
                'email':customer[1]
            },
            'signup': True
        })
@app.route('/signup/<email>/force', methods=['GET'])
def forceSignup(email):
    check = facade.retrieveEmail(email)
    if len(check) > 0:
        # Take the first result
        customer = check[0]
        cio.identify(id=customer[0], email=customer[1], signup=1)
        return jsonify(data={
            'customer':{
                'id':customer[0],
                'email':customer[1]
            },
            'signup':True
        })
    else:
        facade.saveEmail(email)
        result = facade.retrieveEmail(email)
        customer = result[0]

        cio.identify(id=customer[0], email=customer[1], signup=1)
        return jsonify(data={
            'customer':{
                'id':customer[0],
                'email':customer[1]
            },
            'signup': True
        })

@app.route('/customers/<email>/events/<eventname>', methods=['GET'])
def sendEvent(email, eventname):
    customer = facade.retrieveEmail(email)
    if not customer or len(customer) <= 0:
        raise Exception("Customer is not present.")
    customer = customer[0]
    cio.track(customer_id=customer[0], name=eventname)
    return jsonify(data={
        'customer':{
            'id':customer[0],
            'email':customer[1]
        },
        'event':eventname
        'date':
    })

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

