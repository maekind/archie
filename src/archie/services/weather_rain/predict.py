#!/usr/bin/python3
# encoding:utf-8
"""
File that contains prediction class
"""

import dill
import logging
import pandas as pd
from tensorflow.keras.preprocessing import sequence
from keras.models import load_model


class Predict():
    """
    Class that provides methods to predict a sample from a given model
    """

    def __init__(self, model_file, tokenizer_file, text_to_train_header=None, value=[], samples_file=None) -> None:
        """
        Default constructor.
        value or sample_file must be passed as argument to the constructor.
        value is an array with one string.
        sample_file is csv file with headers. Header to predict has to be passed in text_to_train_header.
        """
        # Create logger instance
        self._logger = logging.getLogger("Predict")

        # Set header text to train
        self._text_to_train_header = text_to_train_header

        # Set max text lenght
        self._max_text_lenght = 100  # max lenght for piece of text

        # Set tokenizer file
        self._tokenizer_file = tokenizer_file

        # Set model file
        self._model_file = model_file

        # Prediction parameters
        self._batch_size = 32
        self._verbose = 1

        # Load values
        if len(value) > 0:
            self._sample = value
        elif samples_file:
            self._sample = self._load_samples(samples_file)

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

    def _load_tokenizer(self, tokenizer_file):
        """
        Method to load tokenizer
        """
        self._logger.info("Loading tokenizer ...")
        tokenizer = dill.load(open(tokenizer_file, 'rb'))
        self._logger.info("ok")
        return tokenizer

    def _load_model(self, model_file):
        """
        Method to load tokenizer
        """
        self._logger.info("Loading model ...")
        model = load_model(model_file, compile=False)
        self._logger.info("ok")
        return model

    def _load_samples(self, sample_file):
        """
        Method to load samples from a samples file
        """
        self._logger.info("Loading samples ...")
        test_df = pd.read_csv(sample_file)

        x_test = test_df[self._text_to_train_header].values
        self._logger.info("ok")

        return x_test

    def _tokenize_data(self, x_tokenizer):
        """
        Method to create tokenizer
        """
        self._logger.info("Tokenizing data ...")
        # Tokenize with our pretrained tokenizer to get texts with same lenght
        x_test_tokenized = x_tokenizer.texts_to_sequences(self._sample)

        # Pad the text to have sequences at max lenght of max_test_lenght (400)
        x_testing = sequence.pad_sequences(
            x_test_tokenized, maxlen=self._max_text_lenght)
        self._logger.info("ok")

        return x_testing

    def run(self):
        """
        Method to run prediction
        @return predictions
        """
        # Load model
        model = self._load_model(self._model_file)

        # Load tokenizer
        x_tokenizer = self._load_tokenizer(self._tokenizer_file)

        # Tokenize data
        x_testing = self._tokenize_data(x_tokenizer)

        self._logger.info("Running prediction ...")
        # To predict if our comments are toxic or not
        y_testing = model.predict(
            x_testing, verbose=self._verbose, batch_size=self._batch_size)
        self._logger.info("ok")

        # Return predictions
        return y_testing
