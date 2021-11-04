# encoding:utf-8

"""
listener.py - Handler for listener configuration data in configuration file
"""

from os import path

class ListenerConfig():
    """
    Class to hadle Listener configuration from config file
    """

    def __init__(self, data, data_path):
        """
        Default constructor
        """
        self._language = data["language"]
        self._audio_rate = data["audio_rate"]
        self._adjust_for_noise = data["adjust_for_noise"]
        self._microphone_index = data["microphone_index"]
        self._timeout = data["timeout"]
        self._sounds_path = path.join(data_path, data["sounds_path"])
        self._google_cloud_credentials = path.join(data_path, data["google_cloud_credentials"])

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(language=%r, audio rate=%r, adjust for noise=%r, microphone index=%r, timeout=%r, sounds path=%r" % (
            self.__class__.__name__, self._language, self._audio_rate, self._adjust_for_noise, self._microphone_index, self._timeout, self._sounds_path)

    @property
    def language(self):
        """
        Return language
        """
        return self._language

    @property
    def audio_rate(self):
        """
        Return audio_rate
        """
        return self._audio_rate

    @property
    def adjust_for_noise(self):
        """
        Return adjust_for_noise
        """
        return self._adjust_for_noise

    @property
    def microphone_index(self):
        """
        Return microphone_index
        """
        return self._microphone_index

    @property
    def timeout(self):
        """
        Return timeout
        """
        return self._timeout

    @property
    def sounds_path(self):
        """
        Return sounds_path
        """
        return self._sounds_path

    @property
    def google_cloud_credentials(self):
        """
        Return google_cloud_credentials
        """
        return self._google_cloud_credentials
