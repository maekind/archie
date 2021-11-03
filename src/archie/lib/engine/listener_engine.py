# encoding:utf-8
"""
listener_engine.py - File that contains listener class
"""

import logging
import speech_recognition as sr
from os import path
from playsound import playsound
from archie.utils.decorators import trace_info


class ListenerRecognizerException(Exception):
    """ Custom exception for recognizer """


class ListenerException(Exception):
    """ Custom exception for listener """


class ListenerTimeoutException(Exception):
    """ Custom exception for listener timeout """


class Listener():
    """
    Class to handler the listener
    """

    @trace_info("Initializing listener engine ...")
    def __init__(self, microphone_index, audio_rate, adjust_for_noise, sounds_path, language="es-es") -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger(self.__class__.__name__)
        #self._logger.info("Initializing listener engine ...")
        # Set language
        self._language = language
        # Initialize listener
        self._listener = sr.Recognizer()
        # Set pause threshold
        self._listener.pause_threshold = 2
        # Set microphone adjustment
        self._micro_adjustment = False
        # Set microphone index
        self._micro_index = microphone_index
        # Set sample rate
        self._audio_rate = audio_rate
        # Set adjust for noise flag
        self._adjust_for_noise = adjust_for_noise
        # Set sounds path
        self._sounds_path = sounds_path

        #self._logger.info("ok")

    def listen(self, timeout=None, play_sound=True):
        """
        Method to listen. It returns transcription
        """
        query = ""
        try:
            with sr.Microphone(device_index=self._micro_index) as source:
                self._logger.info("Listenning ...")
                if self._adjust_for_noise:
                    # Set sensitivity
                    self._listener.adjust_for_ambient_noise(source)
                    self._micro_adjustment = True

                # Play listenning sound
                if play_sound:
                    playsound(path.join(self._sounds_path, 'listenning.mp3'))
                # Listenning
                audio = self._listener.listen(source, timeout=timeout)
                self._logger.info("Someone said something!")
        except sr.WaitTimeoutError as e:
            raise ListenerTimeoutException(f"Reached timeout for listener")
        except Exception as e:
            raise ListenerException(f"Unable to open microphone: {e}")

        try:
            self._logger.info("Performing speech to text recognizition ...")
            #query = self._listener.recognize_google(audio, language=self._language)
            query = self._listener.recognize_google_cloud(
                audio, language=self._language)
            self._logger.debug(f"Someone said {query}")

        except sr.RequestError as e:
            self._logger.error(f"Request error: {e}")
        except sr.UnknownValueError as e:
            self._logger.error(f"Unknown value error: {e}")
        except Exception as e:
            raise ListenerRecognizerException(
                f"Unable to recognize your voice: {e}")

        audio.sample_rate = self._audio_rate
        return query.strip(), audio


# Troubleshooting
# The recognizer tries to recognize speech even when I’m not speaking, or after I’m done speaking.
# Try increasing the recognizer_instance.energy_threshold property. This is basically how sensitive the recognizer is to when recognition should start. Higher values mean that it will be less sensitive, which is useful if you are in a loud room.
# This value depends entirely on your microphone or audio data. There is no one-size-fits-all value, but good values typically range from 50 to 4000.
# Also, check on your microphone volume settings. If it is too sensitive, the microphone may be picking up a lot of ambient noise. If it is too insensitive, the microphone may be rejecting speech as just noise.
# The recognizer can’t recognize speech right after it starts listening for the first time.
# The recognizer_instance.energy_threshold property is probably set to a value that is too high to start off with, and then being adjusted lower automatically by dynamic energy threshold adjustment. Before it is at a good level, the energy
# threshold is so high that speech is just considered ambient noise. The solution is to decrease this threshold, or call recognizer_instance.adjust_for_ambient_noise beforehand, which will set the threshold to a good value automatically.
