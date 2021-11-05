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
from archie.config.speaker import SpeakerConfig


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

        # Set paths
        self._conf_path = conf_path
        self._data_path = data_path
        self._services_path = services_path

        # Loads configuration sections
        self._loads()

    def __repr__(self) -> str:
        """ 
        Return a printed version 
        """
        return f"{self.__class__.__name__}, conf path: {self._conf_path}, data path: {self._data_path}, services path: {self._services_path}"

    def _loads(self):
        """
        Loads configuration data into config instansces
        """
        config = yaml.load(
            open(path.join(self._conf_path, 'config.yaml'), 'r'), Loader=yaml.FullLoader)
        self._info = Info(config["info"])
        self._listenerConfig = ListenerConfig(
            config["listener"], self._data_path)
        self._recognitionConfig = RecognitionConfig(
            config["recognition"], self._data_path)
        self._actionsConfig = ActionsConfig(config["actions"], self._data_path)
        self._services = ServicesConfig(
            config["services"], self._services_path)
        self._speakerConfig = SpeakerConfig(config["speaker"])

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

    @property
    def speaker(self):
        """
        Return speaker
        """
        return self._speakerConfig
