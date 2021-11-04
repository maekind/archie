# encoding:utf-8

"""
base.py - Base file for handle configuration
"""

import yaml
from os import path
from archie.config.info import Info
from archie.config.listener import ListenerConfig
from archie.config.recognition import RecognitionConfig
from archie.config.actions import ActionsConfig
from archie.config.services import ServicesConfig


class Configuration():
    """
    Function to handle configuration from file
    """

    def __init__(self, conf_path, data_path, services_path):
        """
        Default constructor
        @data_path: absolute data path
        @conf_path: absolute conf path
        """

        self.__loads(path.join(conf_path, 'config.yaml'), data_path, services_path)

    def __loads(self, config_file, data_path, services_path):
        """
        Loads configuration data into config instansces
        """
        config = yaml.load(open(config_file, 'r'), Loader=yaml.FullLoader)
        self._info = Info(config["info"])
        self._listenerConfig = ListenerConfig(config["listener"], data_path)
        self._recognitionConfig = RecognitionConfig(config["recognition"], data_path)
        self._actionsConfig = ActionsConfig(config["actions"], data_path)
        self._services = ServicesConfig(config["services"], services_path)

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

    @property
    def actions(self):
        """
        Return actions instance
        """
        return self._actionsConfig

    @property
    def services(self):
        """
        Return services
        """
        return self._services
