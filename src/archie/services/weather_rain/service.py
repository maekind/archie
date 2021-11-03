#!/usr/bin/python3
# encoding:utf-8
"""
File that servers weather service
"""
import logging
import uvicorn
import argparse
from os import path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import Predict
from urllib import parse

# Configure logger instance
logger = logging.getLogger("WeatherService")

# Create FastAPI instance
weather = FastAPI()

# Allowed origins
origins = [
    "http://localhost.olympus.com",
    "https://localhost.olympus.com",
    "http://localhost",
    "http://127.0.0.1"
]

# Add middleware
weather.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@weather.get("/predict/{query}")
async def predict(query: str):
    '''
    Function to predict if it is a rain question
    @returns: json string
    '''
    logger.info(f'Query received: {query}')
    predictor = Predict(path.join(path.dirname(__file__), "models", "model_weather_rain.mdl"), 
                        path.join(path.dirname(__file__), "models", "tokenizer_weather_rain.mdl"),
                        "comment_text", value=[parse.unquote_plus(query)])
    # Launch prediction
    predictions = predictor.run()

    # Printing shape
    logger.info(
        f"Shape: {predictions.shape} - Prediction: {predictions[0][0] * 100:.2f}")
    status = False if predictions[0][0] < .5 else True
    logger.info(f"Comment <{query}> is {status}")

    return {"prediction": f"{status}", "Accuracy": f"{predictions[0][0] * 100:.2f}"}


def main():
    '''
    Function Main
    '''
    # Configure arguments
    parser = argparse.ArgumentParser(description="Weather prediction service")
    parser.add_argument('--host',
                        required=True,
                        help="Host where running the service. IP or FQDN.")
    parser.add_argument('--port',
                        help="Port where running the service.",
                        type=int)

    args = parser.parse_args()
    logger.debug(f"Arguments: {args.host}:{args.port}")

    # Launch service
    uvicorn.run("service:weather", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
