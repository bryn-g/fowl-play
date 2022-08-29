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
library(reticulate)
library(voson.tcn)

# standard twitter api v2 bearer token
token <- readRDS("~/.tcn_token")

# use any tweet in conversation
tweet_id <- "https://twitter.com/xxxxxx/status/xxxxxxxxxxxxxxxxx"

# recent conversation thread
thread <- tcn_threads(tweet_id, token = token, endpoint = "recent")

# get conversation users
user_ids <- as.list(thread$users |> distinct(user_id) |> pull())

# reticulate

# if prefer to specify which miniconda - optional
options(reticulate.conda_binary = "D:/PYTHON/miniconda3/condabin/conda.bat")

if (!"r-fowl-play" %in% conda_list()$name) conda_create(envname = "r-fowl-play")
use_condaenv(condaenv = "r-fowl-play")
reqs <- readLines("requirements.txt")
py_install(
  reqs, envname = "r-fowl-play", conda = conda_binary(), pip = TRUE
)

# use more direct get_blt_botscores function
source_python("get_blt_botscores_ret.py")
ret_bot_scores <- get_blt_botscores(
  user_ids = r_to_py(user_ids),
  wait_reset = r_to_py(TRUE)
)

bot_scores <- ret_bot_scores |>
  mutate_at(vars("user_id"), as.character) |>
  # mutate_all(.f = as.character) |>
  as_tibble() |> relocate("user_id") |>
  rename_all(.funs = ~ paste0("bot.", .x)) |>
  distinct(bot.user_id, .keep_all = TRUE)

source("thread_plot_ret.R")

# networks
add_bot_scores <- function(net, bot_scores) {
  if ("user_id" %in% colnames(net$nodes)) {
    net$nodes <- net$nodes |> 
      left_join(bot_scores, by = c("user_id" = "bot.user_id"))
  }
  net
}

# create networks and add bot scores
net_activity <- thread |> tcn_network("activity") |> add_bot_scores(bot_scores)
net_actor <- thread |> tcn_network("actor") |> add_bot_scores(bot_scores)

# thread_net_bot_plot(net_activity)
thread_net_bot_plot(net_actor)
