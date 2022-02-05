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
from urllib import parse
from archie.utils.statistics import SpeechToTextStats

# Configure logger instance
logger = logging.getLogger("MonitorService")

# Create FastAPI instance
monitor = FastAPI()

# Allowed origins
origins = [
    "http://localhost.olympus.com",
    "https://localhost.olympus.com",
    "http://localhost",
    "http://127.0.0.1"
]

# Add middleware
monitor.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@monitor.get("/stats/requests/getcurrent")
async def stats_requests_getcurrent():
    '''
    Function to fetch current month requests
    @returns: json string
    '''
    logger.info(f'Current month requests requested')
    
    val = 0
    res = 0


    # Fetch current month requests
    try:
        # TODO: Change path when installed data in var
        # Initialize statics datababase connection
        stats = SpeechToTextStats(r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/data/db", "statistics.db")

        val = stats.get_current_month_requests()
    except:
        logger.error(f"Unable to fetch requests stats from database")
        res = 1


    return {"val": f"{val}", "res": f"{res}"}

@monitor.get("/stats/requests/update/{query}")
async def stats_requests_update(query):
    '''
    Function to update requests
    @returns: json string
    '''
    logger.info(f'Update requests')

    # TODO: Change path when installed data in var
    # Initialize statics datababase connection
    stats = SpeechToTextStats(r"/Users/marco/Documents/Proyectos/P017-Assistant/archie/data/db", "statistics.db")

    stats.update(parse.unquote_plus(query))

    return {"res": "0"}


def main():
    '''
    Function Main
    '''
    # Configure arguments
    parser = argparse.ArgumentParser(description="Monitor service")
    parser.add_argument('--host',
                        required=True,
                        help="Host where running the service. IP or FQDN.")
    parser.add_argument('--port',
                        help="Port where running the service.",
                        type=int)

    args = parser.parse_args()
    logger.debug(f"Arguments: {args.host}:{args.port}")

    # Launch service
    uvicorn.run("service:monitor", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
