# encoding:utf-8
"""
train_models.py - File that contains training models class for voice recognition
"""

import logging
import numpy as np
import warnings
import _pickle as cPickle
from os import path, walk
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GMM
from archie.lib.recognition.speaker_features import SpeakerFeatures

warnings.filterwarnings("ignore")

__authors__ = "Marco Espinosa"
__license__ = "MIT License"
__version__ = "1.0"
__maintainer__ = "Marco Espinosa"
__email__ = "hi@marcoespinosa.es"
__status__ = "Development"
__credits__ = ["Abhijeet Kumar",
               "Speaker-identification-using-GMMs", "abhijeet.kumar@fmr.com"]

# TODO: Refactor to train only one sample folder passed as argument.


class TrainModels():
    """
    Train models class
    """

    def __init__(self, samples_path, models_path, num_samples) -> None:
        """
        Default constructor
        """
        # Initialize logger name
        self._logger = logging.getLogger("Voice Trainer")
        # Set samples path
        self._samples_path = samples_path
        # Set models path
        self._models_path = models_path
        # Set number of samples to train per speaker
        self._num_samples = num_samples

    def train(self) -> None:
        """
        Method to launch trainning
        """
        count = 1

        # Extracting features for each speaker (5 files per speakers)
        features = np.asarray(())

        self._logger.debug(f"Trainning from {self._samples_path}")

        # Walk in data samples directory
        for dirpath, dirname, filenames in walk(self._samples_path):
            # For each directory, concatenate root path before
            dirnames = map(lambda item: path.join(dirpath, item), dirname)

            # Walk in each samples directory
            for sample_folder in list(dirnames):
                # Walk in sample files
                for _, _, samples in walk(sample_folder):
                    # For each file, concatenate root path before
                    sample_files = map(lambda item: path.join(
                        sample_folder, item), samples)
                    # Get samples folder name from complete path
                    sample_folder_name = path.basename(
                        path.normpath(sample_folder))

                    self._logger.debug(
                        f"Entering sample folder {sample_folder}")
                    # For each file
                    for sample in sample_files:
                        # read the audio
                        sr, audio = read(sample)
                        self._logger.debug(
                            f"Trainning with file {sample} at {sr} rate")
                        # extract 40 dimensional MFCC & delta MFCC features
                        sf = SpeakerFeatures(audio, sr)
                        vector = sf.extract_features()

                        if features.size == 0:
                            features = vector
                        else:
                            features = np.vstack((features, vector))

                        # when features of <num_samples> files of speaker are concatenated, then do model training
                        if count == self._num_samples:
                            gmm = GMM(n_components=16, max_iter=200,
                                      covariance_type='diag', n_init=3)
                            gmm.fit(features)

                            # dumping the trained gaussian model
                            picklefile = path.join(
                                self._models_path, sample_folder_name + ".gmm")
                            self._logger.debug(
                                f"Serialized file: {picklefile}")
                            with open(picklefile, 'wb') as dump:
                                cPickle.dump(gmm, dump)
                                self._logger.info(
                                    f"Modeling completed for speaker: {picklefile} with data point = {features.shape}")
                            features = np.asarray(())
                            count = 0
                        count = count + 1
