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
import pandas as pd
import time
from utils import *


def get_blt_botscores(user_ids, wait_reset = True):
    """ get bot scores for a list of twitter user ids using botometer-lite api endpoint in twitter mode """
    twitter_app_auth, rapid_api_key = get_api_keys()
    blt = botometer.BotometerLite(wait_on_ratelimit=wait_reset, **rapid_api_key, **twitter_app_auth)
    
    res = ()
    i = 1
    for req_user_ids in list(chunks(user_ids, 100)):
        try:
            blt_scores = blt.check_accounts_from_user_ids(req_user_ids)
            res = (*res, pd.DataFrame(blt_scores, columns=["botscore", "user_id"]))
        except Exception as err:
            print(f"{err} - chunk {i}")
        finally:
            pass

        i += 1
        time.sleep(1)

    df = pd.concat(res, ignore_index=True)
    return df
