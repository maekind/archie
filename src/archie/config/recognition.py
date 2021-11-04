# encoding:utf-8

"""
recognition.py - Handler for recognition configuration data in configuration file
"""

from os import path

class RecognitionConfig():
    """
    Class to hadle Recognition configuration from config file
    """

    def __init__(self, data, data_path):
        """
        Default constructor
        """
        self._models_path = path.join(data_path, data["models_path"])
        self._samples_path = path.join(data_path, data["samples_path"])
        self._min_train_samples = data["min_train_samples"]
        self._corpus_path = path.join(data_path, data["corpus_path"])
        self._temp_path = path.join(data_path, data["temp_path"])

    def __repr__(self):
        """
        Return a printed version
        """
        return "%s(models path=%r, samples path=%r, min train samples=%r, corpus path=%r, temp_path=%r)" % (
            self.__class__.__name__, self._models_path, self._samples_path, self._min_train_samples, self._corpus_path, self._temp_path)

    @property
    def models_path(self):
        """
        Return models_path
        """
        return self._models_path

    @property
    def samples_path(self):
        """
        Return samples_path
        """
        return self._samples_path

    @property
    def min_train_samples(self):
        """
        Return min_train_samples
        """
        return self._min_train_samples

    @property
    def corpus_path(self):
        """
        Return corpus_path
        """
        return self._corpus_path

    @property
    def temp_path(self):
        """
        Return temp_path
        """
        return self._temp_path
