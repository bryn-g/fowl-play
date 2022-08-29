library(dplyr)
library(igraph)
library(visNetwork)

# plots
thread_net_bot_plot <- function(net) {
  # labels
  if ("profile.name" %in% colnames(net$nodes)) {
    net$nodes <- net$nodes |>
      mutate(label = paste0(profile.name, " (", bot.botscore, ")"))
  } else {
    net$nodes <- net$nodes |> mutate(label = paste0(bot.botscore))
  }
  
  net$edges <- net$edges |> mutate(label = ifelse(type != "reply", type, NA))
  
  # node color
  net$nodes <- net$nodes |>
    mutate(color = ifelse(is.na(bot.botscore), "#cccccc", "#bb0e6d"),
           opacity = ifelse(is.na(bot.botscore), 0.20, as.double(bot.botscore)))
  
  # actor graph
  g_actor <- graph_from_data_frame(
    net$edges,
    vertices = net$nodes
  ) |>
  visIgraph(idToLabel = FALSE)
  
  g_actor  
}

