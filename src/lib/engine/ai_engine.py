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
        self._listener = Listener(config.listener.microphone_index,
                                  config.listener.audio_rate, config.listener.adjust_for_noise)

        # Initialize speaker engine
        speaker_language = self._language.split(
            '-')[0] + "_" + str.upper(self._language.split('-')[1])
        self._speaker = Speaker(speaker_language)

        # Initialize speaker recognition
        self._speaker_recognition = SpeakerRecognition(
            config.recognition.models_path)

        # Set temporary path
        self._temp_path = config.recognition.temp_path

        # Set initilized to False
        self._init = False

    def run(self):
        """
        Function that launches engine
        """
        # Do speaker recognition tests
        # start_time = time.time()
        # for root, subdirs, filenames in walk(f"../data/samples/Jon-"):
        #     for audio_filename in filenames:
        #         speaker = self._speaker_recognition.find_speaker(f"../data/samples/Jon-/{audio_filename}")
        #         end_time = time.time()
        #         self._logger.info(f"Audio: {audio_filename} | Speaker: {speaker}")
        # self._logger.info(
        #     f"Speaker recognition finished in {(end_time - start_time)} seconds")

        # self._speaker_recognition.force_reload()

        while(True):
            if not self._init:
                self._speaker.say(self._corpus_base.presentation)
                self._init = True
                # TODO: Set init to False after x seconds of inactivity in listenning mode

            # Wait for orders
            query, audio = self._listener.listen()
            #temp_audio_file, fp = self._get_temp_file(audio)
            temp_file = self._get_temp_file(audio)
            
            try:
                speaker = self._speaker_recognition.find_speaker(
                    temp_file)
                self._speaker.say(f"Vale {speaker}")
                # Remove file
                remove(temp_file)
            except Exception as e:
                self._logger.error(e)
                self._speaker.say(self._corpus_base.unknown_speaker)
                # TODO: Pedir si quieres guardar el audio, guardarlo y lanzar trainning y gmm reload!
            
            
            
    def _get_temp_file(self, audio):
        """
        Create a temporary audio file
        """
        audio_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        with open(path.join(self._temp_path, audio_filename), "wb") as temp_file:
            temp_file.write(audio.get_wav_data())
        
        return path.join(self._temp_path, audio_filename)
