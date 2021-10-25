#!/usr/bin/python3
# encoding:utf-8
"""
File that servers weather service
"""
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS


APP = Flask(__name__)
# Only for public services
cors = CORS(APP, resources={r"/api/*": {"origins": "*"}})

# Set logging instance
LOGGER = logging.getLogger("Weather service")

@APP.route('/api/is_rain_question')
def is_rain_question(question):
    '''
    Function to predict if it is a rain question
    @returns: json string
    '''
    LOGGER.info(f'Query received: {question}')

def main():
    '''
    Function Main
    '''
    APP.run(host="localhost", port=32150, debug=False)
    

if __name__ == "__main__":
    main()
    
