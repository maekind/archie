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
        self._timeout = data["timeout"]
        self._witai_key = data["witai_key"]

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(language=%r, audio rate=%r, adjust for noise=%r, microphone index=%r, timeout=%r, wit.ai key=%r" % (
            self.__class__.__name__, self._language, self._audio_rate, self._adjust_for_noise, self._microphone_index, self._timeout, self._witai_key)

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
    def witai_key(self):
        """
        Return witai_key
        """
        return self._witai_key
