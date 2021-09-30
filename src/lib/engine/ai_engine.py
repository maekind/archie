# encoding:utf-8

"""
ai_engine.py - File that contains all ai stuff
"""

import logging
import time
from datetime import datetime
from os import path, walk, remove
from lib.recognition.speaker_recognition import SpeakerRecognition
from config.base import Configuration
from config.corpus import Corpus
from lib.engine.listener_engine import (Listener,
                                        ListenerException, ListenerRecognizerException,
                                        ListenerTimeoutException)
from lib.engine.speaker_engine import Speaker
from lib.engine.step import Step


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
        self._listener = Listener(config.listener.microphone_index,
                                  config.listener.audio_rate, config.listener.adjust_for_noise,
                                  config.listener.witai_key, config.listener.language)

        self._listener_timeout = config.listener.timeout

        # Initialize speaker engine
        speaker_language = self._language.split(
            '-')[0] + "_" + str.upper(self._language.split('-')[1])
        self._speaker = Speaker(speaker_language)

        # Initialize speaker recognition
        self._speaker_recognition = SpeakerRecognition(
            config.recognition.models_path)

        # Set temporary path
        self._temp_path = config.recognition.temp_path

        # Set to init state
        self._state = Step.LISTENING_NOT_ACTIVE

    def run(self):
        """
        Function that launches engine
        """
        
        while(True):

            if self._state == Step.LISTENING_NOT_ACTIVE:
                try:
                    # Wait for orders
                    query, audio = self._listener.listen()
                    
                    # If activation_token:
                    if query and query in self._corpus_base.activation_token.lower():
                        # Create temp file for audio
                        temp_file = self._get_temp_file(audio)
                        try:
                            # Try to recognize speaker
                            speaker = self._speaker_recognition.find_speaker(
                                temp_file)

                            # Saying hello to known speaker
                            self._speaker.say(
                                self._corpus_base.presentation.replace("$speaker$", speaker))

                            # Remove file
                            remove(temp_file)

                        except Exception as e:
                            self._logger.warning(f"Speaker unknown: {e}")
                            # Saying hello to unknown speaker
                            self._speaker.say(
                                self._corpus_base.presentation.replace("$speaker$", ""))

                        # Setting new step to listening active
                        self._state = Step.LISTENING_ACTIVE

                except ListenerException as le:
                    self._logger.error(le)
                    raise ListenerException()
                except ListenerRecognizerException as lre:
                    self._logger.error(lre)

            elif self._state == Step.LISTENING_ACTIVE:
                try:
                    # TODO: Launch timer to stop listenning and jump to LISTENING_NOT_ACTIVE
                    # Wait for orders
                    query, audio = self._listener.listen(
                        timeout=self._listener_timeout)

                except ListenerTimeoutException as lte:
                    self._logger.warning(lte)
                    # Jump to initial state
                    self._state = Step.LISTENING_NOT_ACTIVE

                except ListenerException as le:
                    self._logger.error(le)
                except ListenerRecognizerException as lre:
                    self._logger.error(lre)

                pass
            elif self._state == Step.RECOGNITION:
                pass
            elif self._state == Step.PROCESSING:
                pass
            elif self._state == Step.SPEAKING:
                pass
            elif self._state == Step.TRAINNING:
                pass

    def _get_temp_file(self, audio):
        """
        Create a temporary audio file
        """
        audio_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        with open(path.join(self._temp_path, audio_filename), "wb") as temp_file:
            temp_file.write(audio.get_wav_data())

        return path.join(self._temp_path, audio_filename)
