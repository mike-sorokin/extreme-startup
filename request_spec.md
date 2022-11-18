

# Requests reference
## Error codes
### GET
```
200 - all good
400 - faulty request (bad query parameters)
404 - resource doesnt exist 
```
### POST
```
201 - new resource created
400 - faulty request (bad query params)
```
### PUT
### DELETE

## JSONs
### player
```
{
	"id": string
	"game_id": string
	"name": string
	"score": int
	"api": string - to their entry point
	"events": [list of all event ids]	
	"streak": string		
}
```
### event
```
{
	"id": string //event id
	"player_id": string //player to which event was sent
	"query": string //question sent
	"difficulty": int // 0 for warmup, 1 for round 1, etc...
	"points_gained": int // positive or negative point difference
	"response_type": NO_RESPONSE/WRONG/CORRECT
	"timestamp": RFC3339 //when event was sent
}
```
### game
```
{
	"id": string //game id
	"round": int //0 is warmup, 1..n is difficulty
	"players": [list of player ids]
}
```
## / - main page 
Game management
#### GET - fetch all games
<!-- `-> returns {"games": [list of all game objects] }` -->
`-> returns json of type {(game_id): {game_json}, ...}` with all `game_id` in the json.
#### POST - create new game
```
{ "password": string } 
-> makes a new blank game. returns game json
```
#### PUT - ERROR
ERROR 405
#### DELETE - delete all games
Drops all games, ids, events.

## /(game_id)
Managing a specific game
#### GET - fetch game with this id
`-> returns game json`
#### POST - ERROR
ERROR 405
#### PUT - update game (advance round) or pause
`{"round"} -> updates this game`
`{"pause": (True|False)} -> pauses/unpauses the game`
```
<- {"auto": bool}

returns -> "GAME_AUTO_ON"/"GAME_AUTO_OFF" string
```
#### DELETE - delete game with id
Drops this game, returns `{"deleted": "id"}`

## /(game_id)/assist
#### GET - fetch list of players who need assistance
```
no data to send <-- {}


return --> [playerObjs]

```

## /(game_id)/auth
Managing a specific game
#### GET - fetch game with this id
```
no data to send <-- {}

checking session details...

return --> {
    "authorised": boolean,
    "player": player_id or just ""
}

```
#### POST - ERROR

```
send {"password": string}

validating...

return -> {"valid": boolean}
```

#### PUT - update game (advance round) or pause
Error
#### DELETE - delete game with id
Error

## /(game_id)/players
Managing all players
### GET - fetch game players
`-> returns json of type {(player_id): {player_json}, ...}` with all `player_id` of that game in the json.
### POST - create new player
`sends {"name", "api"}
-> returns newly created player json`
### PUT - ERROR
405
### DELETE - deletes all players in this game

## /(game_id)/players/(player_id)
Managing one player
#### GET - fetch player with this id
`-> returns player json`
#### POST - ERROR
ERROR 405
#### PUT - update player (change name/api, NOT event management)
```
sends {"name" and/or "api"}
-> updates this player, returns new player json
```
#### DELETE - delete player with id
Drops this player, `returns {"deleted": "id"}`

## /(game_id)/players/(player_id)/events
Managing events for this player
### GET - fetch all events
`-> returns {"events": [list of all event objects for this player]}`
### POST - ERROR
405
### PUT - ERROR
405
### DELETE - unacceptable

## /(game_id)/players/(player_id)/events/(event_id)
Managing one event
#### GET - fetch event
`-> returns event json`
#### POST - ERROR
ERROR 405
#### PUT - ERROR
405
#### DELETE - unnacceptable

# REQUESTS FOR GAME REVIEW

## /(game_id)/review/existed

returns true if the game with such id was completed (a.k. stored in database)

### GET

`returns {"existed": boolean}`

Used for Modal which checks the entry for "review game" button form

## /(game_id)/review/finalboard

### GET

```
return array of player stats objects of the form
[
    {
        "player_id": string,
        "name": string,
        "score": int,
        "longest_streak": int,
        "success_ratio": double a.k. successfull requests divided by all requests
        
    },
    {
        "player_id": ...,
        ...
    },
    ...
]
```

## /(game_id)/review/finalgraph

Returns the chart data in the format to be decided.

Since Mike mentioned switching to a different graph library

### GET

```
    TODO
```


## /(game_id)/review/stats

### GET

```
{
    "total_requests": int,
    "average_streak": double // for streaks at least two correct answers in a row,
    "average_on_fire_duration: int (millisec),
    "longest_on_fire_duration": {
        "achieved_by_team": string (name),
        "value": int (millisec),
    },
    "longest_streak": {
        "correct_answers_in_a_row": int,
        "duration": int (millisec)
    },
    "average_success_rate": Double,
    "best_succes_rate":  {
        "achieved_by_team": string (name),
        "value": Double,
    },
    "most_epic_comeback": {
        "achieved_by_team": string (name),
        "points_gained_during_that_streak": int,
        "duration": int (millisec),
        "start_position": int,         // in leaderboard
        "final_achieved_position": int
    },
    "most_epic_fail": {
        "achieved_by_team": string (name),
        "points_lost_during_that_streak": int,
        "duration": int (millisec),
        "start_position": int,         // in leaderboard
        "final_achieved_position": int
    },
    "avg_time_to_solve_new_question": int[] (millisec),
    "time_per_round": int[] (millisec)
}
```

## /(game_id)/review/analysis

Key points of the game

### GET

```

return a array obj[] of json objects of the form:

{
    "title": String,
    "desctiption": 
        | "player X beat previous leader and maintained that position for more than 15 seconds" 
        | "player X became the worst one and maintained that position for more than 15 seconds" 
        | "player X started his epic comeback which was at least 5 seconds long"
        | "player X started his epic fail which was at least 5 seconds long"
        | "Player X glew up and is on fire. d2y/dx2 == very large value"
        | "plyer X was on fire, but now he is fucked. dy/dx < very large negative value"
        | custom,
    "occurence_time": int (millis),
    "achieved_by_team": string (name),   // possibly redundant, because is menrtioned in description
}

```

