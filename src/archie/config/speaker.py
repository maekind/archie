# -*- coding: utf-8 -*-

"""
speaker.py - Handler for speaker data in configuration file
"""


class SpeakerConfig():
    """
    Class to hadle speaker initialization from config file
    """

    def __init__(self, data):
        """
        Default constructor
        """
        self._engine = data["engine"]

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(engine=%r)" % (
            self.__class__.__name__, self._engine)

    @property
    def engine(self):
        """
        Return engine
        """
        return self._engine
