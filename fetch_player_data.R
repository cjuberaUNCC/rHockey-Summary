library(tidyverse)
library(httr)
library(jsonlite)

list_of_api_calls = list()
active_years = 1917:2021
for(x in active_years){
  list_of_api_calls <- append(list_of_api_calls, paste(c("https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster&season=", 
                                                         x, x+1), collapse = ""))
}

all_players = tibble(id = integer(), fullName = character(), link = character())
for (season_api_call in list_of_api_calls) {
  print(season_api_call)
  league = GET(season_api_call)
  league_data = fromJSON(rawToChar(league$content))
  rosters = league_data[["teams"]][["roster"]] 
  for (full_rosters in rosters[[1]]) {
    if (is.null(full_rosters)) {
      next
    } else {
    team = tibble(full_rosters$person)
    all_players <- team %>%
      filter(!(.$id %in% all_players$id)) %>%
      full_join(all_players, .)
    }
  }
}


full_player_with_stats <- all_players
full_player_with_stats$career_goals <- as.integer(NA)
full_player_with_stats$career_points <- as.integer(NA)
full_player_with_stats$career_PIM <- as.integer(NA)

for( player_id in all_players$id){
  print(player_id)
  player_stats_link <- paste(c("https://statsapi.web.nhl.com/api/v1/people/", player_id,"/stats/?stats=yearByYear"), collapse = "")
  player <- GET(player_stats_link)
  player_data <- fromJSON((rawToChar(player$content)))
  
  if("goalAgainstAverage" %in% colnames(player_data$stats$splits[[1]]$stat)) {
    next
  }
  player_data <- tibble(player_data$stats$splits[[1]])
  if(!(133 %in% player_data$league$id)) {
    next
  }
  nhl_season_stats <- player_data %>%
    filter(league$id == 133)
  career_stats <- nhl_season_stats$stat %>%
    summarise(
      "career_goals" = sum(goals, na.rm = TRUE),
      "career_points" = sum(points, na.rm = TRUE),
      "career_PIM" = sum(as.integer(penaltyMinutes), na.rm = TRUE)
    )
  career_stats$id = player_id
  full_player_with_stats <- full_player_with_stats  %>%
    rows_update(career_stats, by = "id")
  
}


full_player_with_stats %>% 
  summarise(
    "total_goals" = sum(career_goals, na.rm = TRUE),
    "total_points" = sum(career_points, na.rm = TRUE),
    "total_PIM" = sum(career_PIM, na.rm = TRUE)
  )
  

write.csv(full_player_with_stats, "NHL_player_career_stats.csv")



