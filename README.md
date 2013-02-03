customerio-restapi
==================

A Flask service for interacting with Customer.io

INSTRUCTION

Clone the repository

Create a virtual environment: virtualenv --distribute venv

Enter the virtual environment: source ./venv/bin/activate

Add the requirements to the environment: pip install -r requirements.txt

Run once sql_init.py: python sql_init.py
This will create the basic table for the api

Register to Customer.IO and get both your site and api keys.
Add the environmental variables siteKey and apiKey
export siteKey=xxxxxx (your site id)
export apiKey=xxxxxx (your api key)

Run foreman start if you want to try the sofware in local.
