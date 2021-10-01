# encoding:utf-8
"""
listener_engine.py - File that contains listener class
"""

from pocketsphinx import Decoder, DefaultConfig
import speech_recognition as sr
import logging

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"


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

    def __init__(self, microphone_index, audio_rate, adjust_for_noise, witai_key, language="es-es") -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger("Listener Engine")
        self._logger.info("Initializing listener engine ...")
        # Set language
        self._language = language
        # Initialize listener
        self._listener = sr.Recognizer()
        # Set pause threshold
        self._listener.pause_threshold = 1
        # Set microphone adjustment
        self._micro_adjustment = False
        # Set microphone index
        self._micro_index = microphone_index
        # Set sample rate
        self._audio_rate = audio_rate
        # Set adjust for noise flag
        self._adjust_for_noise = adjust_for_noise
        # Set Wit.ai key
        self._witai_key = witai_key

        self._logger.info("ok")

    def listen(self, timeout=None) -> str:
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
                
                audio = self._listener.listen(source, timeout=timeout)
                audio.sample_rate = self._audio_rate
                self._logger.info("Someone said something!")
        except sr.WaitTimeoutError as e:
            raise ListenerTimeoutException(f"Reached timeout for listener")
        except Exception as e:
            raise ListenerException(f"Unable to open microphone: {e}")

        try:
            self._logger.info("Performing speech to text recognizition ...")
            # TODO: Uninstall pocketsphinx and swig (from brew) and installa pocketsphinx 0.1.15 from pip.
            # Check the examples at pypi. 
            query = self._listener.recognize_wit(audio, self._witai_key)
            # audio_raw = audio.get_wav_data()
            # with open("../data/temp/audio.wav", "wb") as audio_file:
            #     audio_file.write(audio_raw)
            
            #query = self._speech_to_text()

            #query = self._listener.recognize_sphinx(audio, language=self._language)
            self._logger.debug(f"Someone said {query}")
        except sr.RequestError as e:
            self._logger.error(f"Request error: {e}")
        except sr.UnknownValueError as e:
            self._logger.error(f"Unknown value error: {e}")
        except Exception as e:
            raise ListenerRecognizerException(f"Unable to recognize your voice: {e}")

        print(len(query))

        return query, audio

    def _speech_to_text(self):
        """
        Speech to text conversion
        """
        # Create a decoder with a certain model
        config = DefaultConfig()
        config.set_string('-hmm', '../data/sphinx/es-es/cmusphinx-es-5.2/model_parameters/voxforge_es_sphinx.cd_ptm_4000')
        config.set_string('-lm', '../data/sphinx/es-es/es-20k.lm.gz')
        config.set_string('-dict', '../data/sphinx/es-es/es.dict')
        decoder = Decoder(config)

        # Decode streaming data
        buf = bytearray(1024)
        with open('../data/temp/audio.wav', 'rb') as f:
            decoder.start_utt()
            while f.readinto(buf):
                decoder.process_raw(buf, False, False)
            decoder.end_utt()
        self._logger.debug('Best hypothesis segments:', [seg.word for seg in decoder.seg()])

        

        


# Troubleshooting
# The recognizer tries to recognize speech even when I’m not speaking, or after I’m done speaking.
# Try increasing the recognizer_instance.energy_threshold property. This is basically how sensitive the recognizer is to when recognition should start. Higher values mean that it will be less sensitive, which is useful if you are in a loud room.
# This value depends entirely on your microphone or audio data. There is no one-size-fits-all value, but good values typically range from 50 to 4000.
# Also, check on your microphone volume settings. If it is too sensitive, the microphone may be picking up a lot of ambient noise. If it is too insensitive, the microphone may be rejecting speech as just noise.
# The recognizer can’t recognize speech right after it starts listening for the first time.
# The recognizer_instance.energy_threshold property is probably set to a value that is too high to start off with, and then being adjusted lower automatically by dynamic energy threshold adjustment. Before it is at a good level, the energy
# threshold is so high that speech is just considered ambient noise. The solution is to decrease this threshold, or call recognizer_instance.adjust_for_ambient_noise beforehand, which will set the threshold to a good value automatically.
