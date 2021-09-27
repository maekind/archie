# encoding:utf-8

"""
corpus.py - Contains the class to load the corpus
"""

import json

class Corpus():
    """
    Class to load configured corpus
    """

    def __init__(self, corpus_file) -> None:
        """
        Default constructor
        """
        # Set corpus file
        self._corpus_file = corpus_file

        # Open corpus json file and load it into corpus dict
        self._corpus = dict()

        with open(self._corpus_file, "r") as cfile:
            self._corpus = json.load(cfile)

    @property
    def corpus(self):
        """
        Property corpus
        """
        return self._corpus

    @property
    def presentation(self):
        """
        Property presentation
        """
        return self._corpus.get("presentation")

    @property
    def unknown_speaker(self):
        """
        Property unknown_speaker
        """
        return self._corpus.get("unknown_speaker")

    @property
    def statements(self):
        """
        Property statements
        """
        return self._corpus.get("statements")

    @property
    def negatives(self):
        """
        Property negatives
        """
        return self._corpus.get("negatives")
