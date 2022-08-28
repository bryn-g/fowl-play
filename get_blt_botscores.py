# -*- coding: utf-8 -*-
"""
uses the botometer-lite api endpoint to retrieve bot scores for twitter user ids

- botometer api documentation states that botometer lite uses a lightweight model that allows detection of likely bots
  in bulk.
- unlike botometer-v4, lite just needs the user profile information and the timestamp of when the information was
  collected to perform bot detection.
- twitter mode:
    -- the returned scores reflect the status of the accounts when the bot scores are requested, like with the
       botometer-v4 endpoint
    -- requires a rapid api and twitter api keys
    -- uses botometer-lite check_accounts_from_user_ids function

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
    help="input file of twitter user ids, ensure one id per line",
    required=True
)
@click.option("--wait_reset", "-wr", is_flag=True, help="if api rate-limit reached wait for reset")
def main(file, wait_reset):
    """ get bot scores for a file of twitter user ids using botometer-lite api endpoint in twitter mode """
    # api keys
    twitter_app_auth, rapid_api_key = get_api_keys()
        
    blt = botometer.BotometerLite(wait_on_ratelimit=wait_reset, **rapid_api_key, **twitter_app_auth)

    # read user ids from file and remove duplicates
    f = open(file, "r")
    user_ids = list(map(str, f.read().splitlines()))
    user_ids = list(dict.fromkeys(user_ids))

    # botometer lite api allows 200 requests per day with a max of 100 user ids per request
    # therefore can get botscores for up to 20,000 accounts per day
    res = ()
    i = 1
    for req_user_ids in list(chunks(user_ids, 100)):
        dt_str = get_dt_str()

        try:
            blt_scores = blt.check_accounts_from_user_ids(req_user_ids)

            # save json to file
            with open(f"{dt_str}_blt_chunk_{i}.json", "w", encoding="utf-8") as out:
                json.dump(blt_scores, out, ensure_ascii=False, indent=4)

            res = (*res, pd.DataFrame(blt_scores, columns=["botscore", "user_id"]))
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
