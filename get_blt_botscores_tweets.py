# -*- coding: utf-8 -*-
"""
uses the botometer-lite api to retrieve bot scores for tweets users

- botometer api documentation states that botometer lite uses a lightweight model that allows detection of likely bots
  in bulk.
- non-twitter mode:
    -- if have already collected at least one tweet for each account you want to check can use the non-twitter mode
    -- the returned scores reflect the status of the account when the users tweet was collected
    -- only requires a rapid api key
    -- uses botometer lite check_accounts_from_tweets function

created on Mon Dec 20 18:01:28 2021

@author: bryn-g
"""

import botometer
import click
import json
import pandas as pd
import sys
import time
from utils import *


@click.command()
@click.option(
    "--file", "-f",
    type=click.Path(exists=True),
    help="input file containing list of json dumped tweets",
    required=True
)
@click.option("--wait_reset", "-wr", is_flag=True, help="if api rate-limit reached wait for reset")
def main(file, wait_reset):
    """ get bot scores for tweet users using botometer-lite api endpoint in non-twitter mode """
    # api keys
    rapid_api_key = get_api_keys()[1]

    blt = botometer.BotometerLite(wait_on_ratelimit=wait_reset, **rapid_api_key)

    with open(file, "r", encoding="utf-8") as infile:
        tweets = json.load(infile)

    # botometer lite api allows 200 requests per day with a max of 100 user ids per request
    # therefore can get botscores for up to 20,000 accounts per day
    res = ()
    i = 1
    for tweet_json in list(chunks(tweets, 100)):
        dt_str = get_dt_str()

        try:
            blt_scores = blt.check_accounts_from_tweets(tweet_json)

            # save json to file
            with open(f"{dt_str}_blt_chunk_{i}.json", "w", encoding="utf-8") as out:
                json.dump(blt_scores, out, ensure_ascii=False, indent=4)

            res = (*res, pd.DataFrame(blt_scores, columns=["botscore", "tweet_id", "user_id"]))
        except Exception as err:
            print(f"{err} - chunk {i}")
        finally:
            pass

        i += 1
        time.sleep(1)

    # save scores to csv
    df = pd.concat(res, ignore_index=True)
    df.to_csv(f"{get_dt_str()}_blt_botscores.csv")


if __name__ == "__main__":
    main()
