# author: @bryn-g
# date: 2022-08-26
# ver: 1.0

# collect a twitter conversation thread, use python scripts for bot scores
# add bot scores into networks as node attributes

# options
options(scipen = 999)
options(encoding = "UTF-8")

library(dplyr)
library(readr)
library(voson.tcn)

# standard twitter api v2 bearer token
token <- readRDS("~/.tcn_token")

# use any tweet in conversation
tweet_id <- "https://twitter.com/xxxxxx/status/xxxxxxxxxx"

# recent conversation thread
thread <- tcn_threads(tweet_id, token = token, endpoint = "recent")

# get conversation users
user_ids <- thread$users |> distinct(user_id)

# write user ids to file
write_delim(
  user_ids,
  paste0(voson.tcn:::ids_from_urls(tweet_id), "_user_ids.txt"),
  col_names = FALSE,
  quote = c("none"),
  escape = c("none")
)

# get bot score
# python get_blt_botscores.py -wr -f "xxxxxxxxxx_user_ids.txt"
# or full bot scores
# python get_bv4_botscores.py -wr -f "xxxxxxxxxx_user_ids.txt"

# read bot scores from csv
bot_scores <- read_csv("2022-08-26_225912_bv4_botscores.csv",
                       col_types = cols(.default = "c")) |>
  select(-1, -starts_with("user.user_data")) |>
  rename_all(.funs = ~ paste0("bot.", .x)) |>
  distinct(bot.user_id, .keep_all = TRUE)

# networks
net_with_bot_scores <- function(net, bot_scores) {
  if ("user_id" %in% colnames(net$nodes)) {
    net$nodes <- net$nodes |> 
      left_join(bot_scores, by = c("user_id" = "bot.user_id"))
  }
  net
}

# create networks and add in bot scores
net_activity <- thread |>
  tcn_network("activity") |> net_with_bot_scores(bot_scores)

net_actor <- thread |>
  tcn_network("actor") |> net_with_bot_scores(bot_scores)

# botometer v4 bot scores
names(net_activity$nodes)
# [1] "tweet_id"                                   "conversation_id"                           
# [3] "user_id"                                    "source"                                    
# [5] "created_at"                                 "text"                                      
# [7] "public_metrics.retweet_count"               "public_metrics.reply_count"                
# [9] "public_metrics.like_count"                  "public_metrics.quote_count"                
# [11] "profile.name"                               "profile.username"                          
# [13] "bot.cap.english"                            "bot.cap.universal"                         
# [15] "bot.display_scores.english.astroturf"       "bot.display_scores.english.fake_follower"  
# [17] "bot.display_scores.english.financial"       "bot.display_scores.english.other"          
# [19] "bot.display_scores.english.overall"         "bot.display_scores.english.self_declared"  
# [21] "bot.display_scores.english.spammer"         "bot.display_scores.universal.astroturf"    
# [23] "bot.display_scores.universal.fake_follower" "bot.display_scores.universal.financial"    
# [25] "bot.display_scores.universal.other"         "bot.display_scores.universal.overall"      
# [27] "bot.display_scores.universal.self_declared" "bot.display_scores.universal.spammer"      
# [29] "bot.raw_scores.english.astroturf"           "bot.raw_scores.english.fake_follower"      
# [31] "bot.raw_scores.english.financial"           "bot.raw_scores.english.other"              
# [33] "bot.raw_scores.english.overall"             "bot.raw_scores.english.self_declared"      
# [35] "bot.raw_scores.english.spammer"             "bot.raw_scores.universal.astroturf"        
# [37] "bot.raw_scores.universal.fake_follower"     "bot.raw_scores.universal.financial"        
# [39] "bot.raw_scores.universal.other"             "bot.raw_scores.universal.overall"          
# [41] "bot.raw_scores.universal.self_declared"     "bot.raw_scores.universal.spammer"          
# [43] "bot.user.majority_lang"

# plots
require(igraph)
require(visNetwork)

# activity graph
g_activity <- graph_from_data_frame(
  net_activity$edges, vertices = net_activity$nodes
)
g_activity |> visIgraph()

# actor graph
g_actor <- graph_from_data_frame(
  net_actor$edges, vertices = net_actor$nodes
)
g_actor |> visIgraph()
