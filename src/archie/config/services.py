# encoding:utf-8

"""
services.py - Handler for services configuration data in configuration file
"""

from os import path

class ServicesConfig():
    """
    Class to hadle Services configuration from config file
    """

    def __init__(self, data, services_path):
        """
        Default constructor
        """
        self._python_exe = data["python_exe"]
        self._path = path.join(services_path, data["path"])
        self._services = data["services"]

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(python exe=%r, path=%r, services=%r)" % (
            self.__class__.__name__, self._python_exe, self._path, self._services)

    @property
    def python_exe(self):
        """
        Return python_exe
        """
        return self._python_exe

    @property
    def path(self):
        """
        Return path
        """
        return self._path

    @property
    def services(self):
        """
        Return services
        """
        return self._services
