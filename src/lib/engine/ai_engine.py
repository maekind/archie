# encoding:utf-8

"""
ai_engine.py - File that contains all ai stuff
"""

import logging
from os import path
from config.base import Configuration
from config.corpus import Corpus
from lib.engine.listener_engine import Listener
from lib.engine.speaker_engine import Speaker


class AIEngine():
    """
    Class that contains AI engine methods
    """

    def __init__(self, root_path) -> None:
        """
        Default constructor
        """
        # Set logger name
        self._logger = logging.getLogger("AI Engine")

        # Load configuration
        self._logger.info("Loading configuration ...")
        config = Configuration(root_path)
        self._logger.info("ok")

        # Get corpus path and language to load
        self._corpus_path = config.recognition.corpus_path
        self._language = config.listener.language

        # Load corpus language
        self._logger.info(f"Loading corpus {self._language} ...")
        self._corpus_base = Corpus(
            path.join(self._corpus_path, self._language + ".json"))
        self._logger.info("ok")

        # Initialize listener engine
        self._listener = Listener()

        # Initialize speaker engine
        speaker_language = self._language.split(
            '-')[0] + "_" + str.upper(self._language.split('-')[1])
        self._speaker = Speaker(speaker_language)

    def run(self):
        """
        Function that launches engine
        """
