# -*- coding: utf-8 -*-
"""
uses twarc to retrieve tweet json for tweet ids
json suitable for input into get_blt_botscores_tweets.py

Created on Wed Jan 19 06:53:56 2022

@author: bryn-g
"""

import click
import json
from pathlib import Path
import sys
from twarc import Twarc
from utils import *


@click.command()
@click.option(
    "--file", "-f",
    type=click.Path(exists=True),
    help="input file of tweet ids, ensure one id per line"
)
def main(file):
    """ get tweet json for a file of tweet ids using twarc hydration """
    # api keys
    twitter_app_auth = get_api_keys()[0]
        
    t = Twarc(**twitter_app_auth)

    tweets = list(t.hydrate(open(file, "r")))

    with open(f"{Path(file).with_suffix('.json')}", "w", encoding="utf-8") as out:
        json.dump(tweets, out, ensure_ascii=False)


if __name__ == "__main__":
    main()
