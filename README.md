# fowl-play
Bot scores for Twitter users using the Botometer API.

https://rapidapi.com/OSoMe/api/botometer-pro/details

### Botometer API endpoint scripts

Required modules: `pip install -r requirements.txt`

- `get_blt_botscores.py`: Botometer-Lite (twitter mode, bulk bot scores)
- `get_blt_botscores_tweets.py`: Botometer-Lite (non-twitter mode, provide tweets, bulk bot scores)
- `get_bv4_botscores.py`: Botometer-v4 (full classification and scores)
- `get_tweets.py`: Twarc hydrate tweets from id

#### Botometer-lite API endpoint

```
Usage: get_blt_botscores.py [OPTIONS]

  get bot scores for a file of twitter user ids using botometer-lite api
  endpoint in twitter mode

Options:
  -f, --file PATH    input file of twitter user ids, ensure one id per line
  -wr, --wait_reset  if api rate-limit reached wait for reset
  --help             Show this message and exit.
```

e.g `python get_blt_botscores.py -wr -f user_ids.txt`

#### Input

Line delimited text file of Twitter `user_id`'s (one per line).

#### Output

Saves returned JSON to `json` files and bot scores to a `csv` file with datetime format names.

1. JSON files for each Botometer API response: `2022-08-24_134014_blt_chunk_1.json`, `2022-08-24_134020_blt_chunk_2.json` ...
2. Bot scores for all Twitter users: `2022-08-24_134024_blt_botscores.csv`
```
,botscore,user_id
0,0.08,116889724
...
```

### Twitter and Botometer API Keys

These API key values should be placed in the project workspace `.env` file, replace with your own values after `=`:

```
TWITTER_CONSUMER_KEY= ...
TWITTER_CONSUMER_SECRET= ...
RAPID_BOTOMETER_API_KEY= ...
```

https://github.com/IUNetSci/botometer-python#authentication

