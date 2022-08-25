# -*- coding: utf-8 -*-
"""
helper functions

created on Fri Jan 21 07:01:16 2022

@author: bryn-g
"""

import os
from datetime import datetime as dt
from dotenv import load_dotenv

def get_api_keys():
    """ get api key values from .env file """
    load_dotenv()
    twitter_app_auth = {
        "consumer_key": os.environ.get("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.environ.get("TWITTER_CONSUMER_SECRET") #,
        # "access_token": os.environ.get("TWITTER_ACCESS_TOKEN"),
        # "access_token_secret": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    }
    rapid_api_key = {
        "rapidapi_key": os.environ.get("RAPID_BOTOMETER_API_KEY")
    }
    return twitter_app_auth, rapid_api_key


def get_dt_str():
    """ get formatted datetime string from current timestamp """
    return f"{dt.now().strftime('%Y-%m-%d_%H%M%S')}"


def chunks(values, n):
    """ return chunks of n size from values """
    for i in range(0, len(values), n):
        yield values[i:i + n]
