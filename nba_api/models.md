# Models

## Team
```
$ Team
  * id
  - city
  - nickname
  - full_name
  - short_name
  - logo
  - all_star
  - nba_franchise
  & leagues
```

## Player
```
$ Player
  * id
  - first_name
  - last_name
  & team_id
  - years_pro
  - college_name
  - country
  - player_id
  - date_of_birth
  - affiliation
  - start_nba
  - height_in_meters
  - weight_in_kilograms
  & leagues
```

## Game
```
$ Game
  * id
  - season_year
  - league
  - start_time_utc
  - end_time_utc
  - arena
  - city
  - country
  - clock
  - game_duration
  - current_period
  - halftime
  - end_of_period
  - season_stage
  - status_short_game
  - status_game
  & home_id
  - home_score
  & away_id
  - away_score
```

## League
```
$ Leauge
  * id
  - conference
  - division
  - jersey
  - active
  - position
```

## Team Statistics
```
$ TeamStats
  & game_id
  & team_id
  - fast_break_points
  - points_in_paint
  - biggest_lead
  - second_chance_points
  - points_off_turnovers
  - longest_run
  - points
  - fgm
  - fga
  - fgp
  - ftm
  - fta
  - ftp
  - tpm
  - tpa
  - tpp
  - off_reb
  - def_reb
  - tot_reb
  - assists
  - p_fouls
  - steals
  - turnovers
  - blocks
  - plus_minus
  - min
```

## Player Statistics
```
$ PlayerStats
  & game_id
  & team_id
  & player_id
  - points
  - pos
  - min
  - fgm
  - fga
  - fgp
  - ftm
  - fta
  - ftp
  - tpm
  - tpa
  - tpp
  - off_reb
  - def_reb
  - tot_reb
  - assists
  - p_fouls
  - steals
  - turnovers
  - blocks
  - plus_minus
```
