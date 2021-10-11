# encoding:utf-8

"""
ai_engine.py - File that contains all ai stuff
"""

import logging
from datetime import datetime
from os import path, remove
from lib.actions.weather import WeatherInterface
from lib.recognition.speaker_recognition import SpeakerRecognition
from config.base import Configuration
from config.corpus import Corpus
from lib.engine.listener_engine import (Listener,
                                        ListenerException, ListenerRecognizerException,
                                        ListenerTimeoutException)
from lib.engine.speaker_engine import Speaker
from lib.engine.step import Step
from lib.actions.rae import RaeInterface


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
                                  config.listener.sounds_path, config.listener.language)

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
        # Set actions config instance
        self._actions_config = config.actions
        
        # Set to init state
        self._state = Step.LISTENING_NOT_ACTIVE

    def run(self):
        """
        Function that launches engine
        """
        # Initialize what archi says variable
        ai_says = ""
        play = True

        while(True):

            if self._state == Step.LISTENING_NOT_ACTIVE:
                self._logger.debug(f"Step: LISTENING_NOT_ACTIVE")
                try:
                    # Wait for orders
                    query, audio = self._listener.listen(play_sound=False)

                    # If activation_token:
                    if query and query.lower() in self._corpus_base.activation_tokens:
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
                    else:
                        self._logger.warning("Activation token not found!")
                        self._logger.warning(
                            "Archi speaking: 'For activation say \"Hola Archi\"'")

                except ListenerException as le:
                    self._logger.error(le)
                    raise ListenerException()
                except ListenerRecognizerException as lre:
                    self._logger.error(lre)

            elif self._state == Step.LISTENING_ACTIVE:
                self._logger.debug(f"Step: LISTENING_ACTIVE")
                try:
                    # Wait for orders
                    query, audio = self._listener.listen(
                        timeout=self._listener_timeout,
                        play_sound=play)

                    self._state = Step.PROCESSING

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
                self._logger.debug(f"Step: RECOGNITION")
                pass
            elif self._state == Step.PROCESSING:
                self._logger.debug(f"Step: PROCESSING")
                found = False
                self._logger.info(f"Searching for action in {query}")
                # Serching for query in defined actions
                for key, action in self._corpus_base.actions.items():
                    if key in query.lower():
                        found = True
                        self._logger.info(f"Action {action} found!")
                        self._launch_action(action, query)
                        # Jump to listenning active state
                        self._state = Step.LISTENING_ACTIVE
                        play = False

                if not found:
                    self._logger.warning(f"Action {action} not found!")
                    ai_says = self._corpus_base.unknown_action
                    self._state = Step.SPEAKING

            elif self._state == Step.SPEAKING:
                self._logger.debug(f"Step: SPEAKING")
                self._logger.info(f"AI speaking...")
                # ai says something
                self._speaker.say(ai_says)
                # Jump to listenning active state
                self._state = Step.LISTENING_ACTIVE

            elif self._state == Step.TRAINNING:
                self._logger.debug(f"Step: TRAINNING")
                pass

    def _get_temp_file(self, audio):
        """
        Create a temporary audio file
        """
        audio_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        with open(path.join(self._temp_path, audio_filename), "wb") as temp_file:
            temp_file.write(audio.get_wav_data())

        return path.join(self._temp_path, audio_filename)

    def _launch_action(self, action, query):
        """
        Method to launch defined actions
        """

        if action == "rae":
            self._logger.debug("rae action detected!")
            self._rae_action(query)
        elif action == "time":
            self._logger.debug("time action detected!")
            self._logger.warning("Not implemented yet!")
            
        elif action == "weather":
            self._logger.debug("weather action detected!")
            self._logger.warning("Not implemented yet!")
            
            
    def _rae_action(self, query):
        """
        Method to launch RAE IA engine
        """
        rae = RaeInterface()
        definitions = rae.search(query.split(' ')[-1])

        if definitions is not None:
            self._logger.debug(f"definitions: {definitions}")

            # Say definition found
            self._speaker.say(self._corpus_base.found)
            definitions_count = len(definitions)
            definitions_said = 0
            next = True

            self._logger.debug(
                f"Number of definitions: {definitions_count}")

            # Iterate definitions
            for definition in definitions:
                # Tell definition
                if next:
                    self._speaker.say(definition.get("definition"))
                    definitions_said += 1
                    # If there are more defintions:
                    if definitions_said < definitions_count:
                        # Question if ai continues telling definitions
                        self._speaker.say(
                            self._corpus_base.more_definitions)

                        query, _ = self._listener.listen()
                        # Checking for a statement in query
                        for word in query.split(' '):
                            next = False
                            if word in self._corpus_base.statements:
                                next = True
                                break
                else:
                    # No more defintions ...
                    self._speaker.say(
                            self._corpus_base.ok)
                    break        
        # Word not found or error
        else:
           self._speaker.say(
                            self._corpus_base.nothing_found) 

    def _weather_action(self, query):
        """
        Method to retrive weather info
        """
        weather = WeatherInterface(self._actions_config.openweather_key)
        

    def _time_action(self):
        """
        Method to get actual time
        """