# encoding:utf-8

"""
listener.py - Handler for listener configuration data in configuration file
"""


class ListenerConfig():
    """
    Class to hadle Listener configuration from config file
    """

    def __init__(self, data):
        """
        Default constructor
        """
        self._language = data["language"]
        self._audio_rate = data["audio_rate"]
        self._adjust_for_noise = data["adjust_for_noise"]
        self._microphone_index = data["microphone_index"]

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(language=%r, audio rate=%r, adjust for noise=%r, microphone inde=%r" % (
            self.__class__.__name__, self._language, self._audio_rate, self._adjust_for_noise, self._microphone_index)

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
