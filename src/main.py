# -*- coding: utf-8 -*-
"""
File that contains main tests
"""
import logging
import sys
import time
from os import path, walk
from datetime import datetime

from speech_recognition import AudioData
from lib.recognition.train_models import TrainModels
from lib.recognition.speaker_recognition import SpeakerRecognition
from lib.engine.listener_engine import Listener, ListenerRecognizerException

from lib.engine.ai_engine import AIEngine

def configure_logger():
    """
    Method to configure logging
    """
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = "DEBUG"

    logging.basicConfig(**logargs)

    return logging.getLogger("Main")


def main():
    """
    Main function
    """
    # Configure logger
    logger = configure_logger()

    # TODO:  Get some samples for trainning models

    # TODO:  Same samples into a data folder

    # set speaker
    speaker_name = "Marco"

    # Testing Listener engine
    # listener = Listener()
    # for i in range(1,5):
    #     try:
    #         audio : AudioData
    #         query, audio = listener.listen()
    #         logger.info(f"Catched: {query}")

    #         audio_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
    #         with open(path.join(f"../data/samples/{speaker_name}-", audio_filename), "wb") as audio_file:
    #             audio.sample_rate = 16000
    #             audio_file.write(audio.get_wav_data())
    #     except ListenerRecognizerException as e:
    #         logger.warning(
    #             "mmmm ... It seams that you said something, but it has not been recognized ... Try again!")

    # # Train test models
    # train = TrainModels("../data/samples", "../data/models", 1)
    # logger.info("Lauching trainning models task ...")
    # start_time = time.time()
    # train.train()
    # end_time = time.time()
    # logger.info(f"Tranning finished in {(end_time - start_time)} seconds")

    # TODO: Get a new sample to launch recognition

    # TODO: Pass new sample to speaker recognition

    # Do speaker recognition tests
    # sr = SpeakerRecognition("../data/models")
    # #logger.info(f"Launching speaker recognition tests with file {audio_filename}...")
    # start_time = time.time()
    # for root, subdirs, filenames in walk(f"../data/samples/{speaker_name}-"):
    #     for audio_filename in filenames:
    #         speaker = sr.find_speaker(f"../data/samples/{speaker_name}-/{audio_filename}")
    #         end_time = time.time()
    #         logger.info(
    #             f"Speaker recognition finished in {(end_time - start_time)} seconds")
  
    try:
        archi = AIEngine(path.dirname(__file__))
        archi.run()
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
