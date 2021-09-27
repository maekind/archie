# encoding:utf-8

"""
base.py - Base file for handle configuration
"""

import yaml
from os import path
from config.info import Info
from config.listener import ListenerConfig
from config.recognition import RecognitionConfig


class Configuration():
    """
    Function to handle configuration from file
    """

    def __init__(self, base_path):
        """
        Default constructor
        @base_path: absolute script path
        """

        self.__loads(path.join(base_path, 'config.yaml'))

    def __loads(self, config_file):
        """
        Loads configuration data into config instansces
        """
        config = yaml.load(open(config_file, 'r'), Loader=yaml.FullLoader)
        self._info = Info(config["info"])
        self._listenerConfig = ListenerConfig(config["listener"])
        self._recognitionConfig = RecognitionConfig(config["recognition"])

    @property
    def info(self):
        """
        Return info instance
        """
        return self._info

    @property
    def listener(self):
        """
        Return info listener
        """
        return self._listenerConfig

    @property
    def recognition(self):
        """
        Return recognition instance
        """
        return self._recognitionConfig
