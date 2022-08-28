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

# create network
net_actor <- thread |> tcn_network("actor")

# add bot scores
net_actor$nodes <- net_actor$nodes |>
  left_join(bot_scores, by = c("user_id" = "bot.user_id"))

  # plots
require(igraph)
require(visNetwork)

pal <- colorRampPalette(c('#f1dde0','#bb0e6d'))
net_actor$nodes$color <- pal(8)[cut(net_actor$nodes$bot.botscore, breaks = 8)]
net_actor$nodes$label <- paste0(
  net_actor$nodes$profile.name,
  " (", as.character(net_actor$nodes$bot.botscore), ")"
)
net_actor$nodes <- net_actor$nodes |>
  mutate(color = ifelse(is.na(color), "#f5f5f5", color))

# actor graph
g_actor <- graph_from_data_frame(
  net_actor$edges, vertices = net_actor$nodes
) |>
visIgraph(idToLabel = FALSE)

g_actor
