#!/usr/bin/python3
# encoding:utf-8
"""
File that contains trainning test in a convolutional neural network
"""

import dill
import logging
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import text, sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, MaxPooling1D
from sklearn.model_selection import train_test_split


class Train():
    """
    Class that contains methods to train a model with a samples CSV file
    """

    def __init__(self, samples_file, text_to_train_header, values_to_train_header,
                 embeddings_file, embeddings_dim, csv_sep=',') -> None:
        """
        Default constructor
        """
        # Create logger instance
        self._logger = logging.getLogger("Train")
        # Set samples file to train
        self._samples_file = samples_file
        # Set header text to train
        self._text_to_train_header = text_to_train_header
        # Set header values to train
        self._values_to_train_header = values_to_train_header
        # Set embeddings file
        self._embeddings_file = embeddings_file
        # Set csv separator
        self._csv_sep = csv_sep

        # Hyperparameters optimization
        self._max_features = 20000  # max words to keep from dataset
        self._max_text_lenght = 100  # max lenght for piece of text
        self._filters = 250  # Max number of output channels in convolution layer (Original 250)
        self._kernel_size = 3 # Filter with or lenght. One number because is a one dim convolution (Original 3)
        self._hidden_dims = 150  # Hidden dims for layers (Original 250)
        self._batch_size = 10  # Number of examples to training at one time (original 32)
        self._epochs = 5  # How many times we pass over the trained data (Original 3)
        self._embedding_dim = embeddings_dim

    def __repr__(self) -> str:
        """ Return a printed version """
        return f"{self.__class__.__name__}"

    def run(self):
        """
        Method to launch training
        """

        # Load samples into a data frame
        self._load_samples()

        # Create tokenizer and padding data
        x_values_train = self._tokenize_data()

        # Load embeddings
        embeddings_index = self._prepare_embeddings()

        # Create embedding matrix
        embedding_matrix = self._create_embedding_matrix(embeddings_index)

        # Create model
        model = self._create_model(embedding_matrix)

        # Compile model
        model = self._compile_model(model)

        # Train model
        model = self._train_model(
            model, x_values_train, self._y_values, self._batch_size, self._epochs)

        # Saving model as a class var
        self._model = model

        return model.history

    def _load_samples(self):
        """
        Method to load samples to train
        """
        self._logger.info("Loading samples ...")
        # Load data into the data frame
        self._train_df = pd.read_csv(self._samples_file, sep=self._csv_sep).fillna(' ')
        
        # Sheffle data!
        self._train_df = self._train_df.sample(frac=1).reset_index(drop=True)

        # Get text and values to train
        self._x_values = self._train_df[self._text_to_train_header].values
        self._y_values = self._train_df[self._values_to_train_header].values

        self._logger.info("ok")

        self._logger.debug(
            f"{self._train_df[self._text_to_train_header].value_counts()}")
        self._logger.debug(
            f"{self._train_df[self._values_to_train_header].value_counts()}")

    def _tokenize_data(self):
        """
        Method to create tokenizer
        """
        self._logger.info("Tokenizing data ...")
        # Create a tokenizer
        self._x_tokenizer = text.Tokenizer(self._max_features)
        self._x_tokenizer.fit_on_texts(list(self._x_values))
        x_tokenized = self._x_tokenizer.texts_to_sequences(
            self._x_values)  # tokenize text in numbers (integers)

        # Padding values to train
        x_values_train = sequence.pad_sequences(
            x_tokenized, maxlen=self._max_text_lenght)

        # TODO: I don't know if I have to recalculate features here or not!
        # Set max features from tokenizer
        self._max_features = len(self._x_tokenizer.word_index) + 1 

        self._logger.info("ok")

        return x_values_train

    def _prepare_embeddings(self):
        """
        Method to load embeddings
        """
        self._logger.info("Preparing embeddings ...")
        embeddings_index = dict()
        f = open(self._embeddings_file)

        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs  # map embeddings dict

        f.close()
        self._logger.info("ok")
        self._logger.debug(f"Found {len(embeddings_index)} word vectors.")

        return embeddings_index

    def _create_embedding_matrix(self, embeddings_index):
        """
        Method to create the embedding matrix
        """
        embedding_matrix = np.zeros((self._max_features, self._embedding_dim))
        for word, index in self._x_tokenizer.word_index.items():
            if index > self._max_features - 1:
                break
            else:
                embedding_vector = embeddings_index.get(word)
                if embedding_vector is not None:
                    embedding_matrix[index] = embedding_vector

        return embedding_matrix

    def _create_model(self, embedding_matrix):
        """
        Method to create model.
        """
        self._logger.info("Creating model ...")
        model = Sequential()

        # Mapping vocabulary indexes into the embedding dimensions
        model.add(Embedding(self._max_features,
                            self._embedding_dim,
                            embeddings_initializer=tf.keras.initializers.Constant(
                                embedding_matrix),
                            trainable=False))

        # trainable=False because we don't want to update the embeddings weights during training
        # Add Dropout regularization
        model.add(Dropout(0.2))

        model.add(Conv1D(self._filters,
                         self._kernel_size,
                         padding='valid'))
        # padding='valid' to not padding the data because we have already padded it

        model.add(MaxPooling1D())
        model.add(Conv1D(self._filters,
                         self._kernel_size,
                         padding='valid',
                         activation='relu'
                         ))
        model.add(GlobalMaxPooling1D())  # Download the samples to max
        model.add(Dense(self._hidden_dims, activation='relu'))
        model.add(Dropout(0.2))  # To prevent overfitting
        # Gives us a value between 0 and 1
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        return model

    def _compile_model(self, model):
        """
        Method to compile the model
        """
        self._logger.info("Compiling model ...")
        model.compile(loss='binary_crossentropy',
                      optimizer='adam', metrics=['accuracy'])
        self._logger.info("ok")

        return model

    def _train_model(self, model, x_values_train, y_values, batch_size, epochs):
        """
        Method to train the model
        """
        self._logger.info("Trainning model ...")
        # Split data into training and validation sets
        # 0.15 to use only the 15% of our data
        # x_train_val=comments padded from tokenized and y=toxic values
        x_train, x_val, y_train, y_val = train_test_split(x_values_train, y_values,
                                                          test_size=0.15, random_state=1)

        model.fit(x_train, y_train, batch_size=batch_size,
                  epochs=epochs,
                  validation_data=(x_val, y_val))

        self._logger.info("ok")

        return model

    def save_model(self, model_file):
        """
        Method to save trainned model in to a pickel file
        """

        self._logger.info(f"Saving model to {model_file} ...")
        # Save model
        self._model.save(model_file, overwrite=True,
                         include_optimizer=True, save_format='h5')
        self._logger.info("ok")

    def save_tokenizer(self, tokenizer_file):
        """
        Method to save tokenizer in to a pickel file
        """

        self._logger.info(f"Saving tokenizer to {tokenizer_file} ...")
        # Save tokenizer
        dill.dump(self._x_tokenizer, open(tokenizer_file, 'wb'))
        self._logger.info("ok")
