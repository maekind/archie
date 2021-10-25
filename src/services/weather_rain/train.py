#!/usr/bin/python3
# encoding:utf-8
"""
Main file to test trainning and prediction
"""

import logging
from trainning import Train
from predict import Predict
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Setting application logging level
LOG_LEVEL = "INFO"


def configure_logger():
    """
    Method to configure logging
    """
    logargs = {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'}

    logargs["level"] = LOG_LEVEL

    logging.basicConfig(**logargs)

    return logging.getLogger("CNN main")

def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    x = range(1, len(acc) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x, acc, 'b', label='Training accuracy')
    plt.plot(x, val_acc, 'r', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(x, loss, 'b', label='Training loss')
    plt.plot(x, val_loss, 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

def main():
    """
    Main program
    """
    # Configure logger
    logger = configure_logger()

    # Rain tests
    train_for_rain_question()
    check_for_rain_question(logger)
    

def train_for_rain_question():
    """
    Method to train models for rain questions
    """
    # Trainning model on toxic comments
    train = Train("data/train.csv", "comment_text",
                  "rain", "data/SBW-vectors-300-min5.txt", 300, csv_sep=';')

    # Launch trainning
    history = train.run()

    # Save model to use it later for prediction
    train.save_model("models/model_weather_rain.mdl")

    # Save tokenizer to use it later for prediction
    train.save_tokenizer("models/tokenizer_weather_rain.mdl")

    plot_history(history)

def check_for_rain_question(logger):
    """
    Method that launches rain question tests prediction
    """
    # Testing prediction with test.csv
    # predict = Predict("models/model_toxic.mdl", "models/tokenizer_toxic.mdl",
    #                   "comment_text", samples_file="data/test.csv")
    # Testing prediction with one sentence
    comment = 'La lluvia de Galicia es algo molesta'
    predict_rain_question(comment, logger)
    comment = '¿Lloverá dentro de dos días?'
    predict_rain_question(comment, logger)
    comment = 'La lluvia de los Pirineos suele ser abundante'
    predict_rain_question(comment, logger)
    comment = '¿Me pregunto si lloverá mucho en Mallorca?'
    predict_rain_question(comment, logger)
    comment = '¿Crees que mañana lloverá?'
    predict_rain_question(comment, logger)
    comment = '¿El fin de semana que viene lloverá?'
    predict_rain_question(comment, logger)
    comment = '¿Lloverá el domingo por la tarde?'
    predict_rain_question(comment, logger)
    comment = '¿El jueves por la mañana lloverá mucho?'
    predict_rain_question(comment, logger)
    comment = 'La lluvia en Cerdanyola puede ser abundante, ¿No crees?'
    predict_rain_question(comment, logger)
    comment = '¿El viernes por la tarde lloverá en Algeciras?'
    predict_rain_question(comment, logger)
    comment = '¿El lunes habrá tormenta?'
    predict_rain_question(comment, logger)
    comment = 'Si llueve me quedaré en casa'
    predict_rain_question(comment, logger)
    comment = '¿Tienes un paragüas por si llueve?'
    predict_rain_question(comment, logger)

def predict_rain_question(comment, logger):
    """
    Method to predict a sample status
    """
    predict = Predict("models/model_weather_rain.mdl", "models/tokenizer_weather_rain.mdl",
                       "comment_text", value=[comment])
    # Launch prediction
    predictions = predict.run()

    # Printing shape
    logger.info(f"Shape: {predictions.shape} - Prediction: {predictions[0][0] * 100:.2f}")
    status = "Not rain question" if predictions[0][0] < .5 else "Rain question"
    logger.info(f"Comment <{comment}> is {status}")

if __name__ == "__main__":
    main()
