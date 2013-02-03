import os
import uuid
from customerio import CustomerIO
from flask import Flask, jsonify, json
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException, NotFound
from dbFacade import DBFacade
import datetime

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

def parseCustomerObject(customer):
    """
    Parse the returned data given a customer in input
    :param customer:
    :return:
    """
    return {
        'customer':{
            'id':customer[0],
            'email':customer[1]
        },
        'date':datetime.datetime.utcnow().isoformat()
    }

def __signupCustomer(email, contactCustomerIO=False):
    """
    Lookup a customer by email and it adds to the database if it is not present.
    It contacts Customer.IO if the customer is inserted in the database or contactCustomerIO is true
    :param email: The customer's email
    :param contactCustomerIO: True if the service is forced to contact Customer.IO, false otherwise
    :return: The returned data
    """
    customer = facade.retrieveEmail(email)
    signup = contactCustomerIO
    if not customer:
        facade.saveEmail(email)
        customer = facade.retrieveEmail(email)
        signup = True

    data = parseCustomerObject( customer )
    # Additional information
    data['signup'] = signup

    if signup:
        # Contact Customer.Io
        cio.identify(id=customer[0], email=customer[1], signup=signup)
    return data

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/signup/<email>', methods=['GET'])
def signupCustomer(email):
    """
    It signup a customer and contact Customer.IO if the customer is not present in the db
    :param email: The Customer's email
    :return:The returned json data
    """
    data = __signupCustomer(email)
    # Return the data
    return jsonify(data=data)

@app.route('/signup/<email>/force', methods=['GET'])
def forceSignup(email):
    """
    It signup a customer and contact Customer.IO if the customer is not present in the db
    :param email: The Customer's email
    :return:The returned json data
    """
    data = __signupCustomer(email, True)
    # Return the data
    return jsonify(data=data)


@app.route('/customers/<email>/events/<eventname>', methods=['GET'])
def sendEvent(email, eventname):
    """
    It send an event for a given customer's email. It contact Customer.IO given the event's name
    :param email: The customer's email
    :param eventname: The event name
    :return: The returned json data
    """
    customer = facade.retrieveEmail(email)
    if not customer:
        raise Exception("Customer is not present.")

    cio.track(customer_id=customer[0], name=eventname)

    data = parseCustomerObject(customer)
    data['event'] = eventname

    return jsonify(data=data)

if  __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

