# encoding:utf-8

"""
model.py - File that contains web service class model
"""

import requests
from typing import Tuple
from urllib import parse


class ServiceInterface:
    """
    Class that modelize a web service
    """

    def __init__(self, name: str, config: Tuple) -> None:
        """
        Default constructor
        """
        # Set service name
        self._name = name
        # Set service configuration from Tuple
        self._host, self._port = config

        self._url = f"http://{self._host}:{self._port}"
        
    @property
    def Name(self):
        """ Name property """
        return self._name

    @property
    def Host(self):
        """ Host property """
        return self._host

    @property
    def Port(self):
        """ Port property """
        return self._port
    
    def query(self, query) -> bool:
        """
        Method to send a query to service
        """
        parameter = parse.quote_plus(query)
        res = requests.get(self._url + f"/predict/{parameter}")

        print(res)
            
        return False
        
