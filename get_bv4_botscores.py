# -*- coding: utf-8 -*-
"""
uses the botometer-v4 api endpoint to retrieve bot scores for user ids

created on Thu Jan 20 08:33:00 2022

@author: bryn-g
"""

import botometer
import click
import json
import pandas as pd
import time
from utils import *


@click.command()
@click.option(
    "--file", "-f",
    type=click.Path(exists=True),
    help="input file of twitter user ids, ensure one id per line"
)
@click.option("--wait_reset", "-wr", is_flag=True, help="if api rate-limit reached wait for reset")
def main(file, wait_reset):
    """ get bot scores for a file of twitter user ids using botometer-v4 api endpoint """
    # api keys
    twitter_app_auth, rapid_api_key = get_api_keys()

    b = botometer.Botometer(wait_on_ratelimit=wait_reset, **rapid_api_key, **twitter_app_auth)

    # read user ids from file and remove duplicates
    f = open(file, "r")
    user_ids = list(map(str, f.read().splitlines()))
    user_ids = list(dict.fromkeys(user_ids))

    res = ()
    i = 1
    for req_user_ids in list(chunks(user_ids, 100)):
        dt_str = get_dt_str()

        try:
            b_scores = dict(b.check_accounts_in(req_user_ids))

            # save json to file
            with open(f"{dt_str}_bv4_chunk_{i}.json", "w", encoding="utf-8") as out:
                json.dump(list(b_scores.values()), out, ensure_ascii=False, indent=4)

            df = pd.json_normalize(b_scores.values())
            df.insert(0, "user_id", req_user_ids)
            res = (*res, df)
        except Exception as err:
            print(f"{err} - chunk {i}")
        finally:
            pass

        i += 1
        time.sleep(1)

    # save scores to csv
    df = pd.concat(res, ignore_index=True)
    df.to_csv(f"{get_dt_str()}_bv4_botscores.csv")


if __name__ == "__main__":
    main()
