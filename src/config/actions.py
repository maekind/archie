# encoding:utf-8

"""
actions.py - Handler for actions configuration data in configuration file
"""


class ActionsConfig():
    """
    Class to hadle Actions configuration from config file
    """

    def __init__(self, data):
        """
        Default constructor
        """
        with open(data["openweather_key"], "r") as key:
            self._openwheater_key = key.read().get("key")

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(open weather key=%r" % (
            self.__class__.__name__, self._openwheater_key)

    @property
    def openweather_key(self):
        """
        Return openweather_key
        """
        return self._openweather_key
