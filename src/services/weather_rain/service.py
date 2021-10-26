#!/usr/bin/python3
# encoding:utf-8
"""
File that servers weather service
"""
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

weather = FastAPI()

origins = [
    "http://localhost.olympus.com",
    "https://localhost.olympus.com",
    "http://localhost",
    "http://127.0.0.1"
]

weather.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set logging instance
LOGGER = logging.getLogger("Weather service")

@weather.get("/predict/{query}")
async def predict(query: str):
    '''
    Function to predict if it is a rain question
    @returns: json string
    '''
    LOGGER.info(f'Query received: {query}')
    return {"query": query}
    
    

def main():
    '''
    Function Main
    '''
    uvicorn.run("service:weather", host="127.0.0.1", port=32152)
    
if __name__ == "__main__":
    main()
    
