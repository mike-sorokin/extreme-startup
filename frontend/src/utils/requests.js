import axios from 'axios';

import { homeAPI, gameAPI, playersAPI, playerAPI, playerEventsAPI, eventAPI, home } from "./urls"
import { alertError, showFailureNotification } from './utils';

const instance = axios.create({
  headers: { 'Content-Type': 'application/json', }
})

/**
 * Object representing a Player
 * @typedef {Object} Player
 * @property {String} id
 * @property {String} game_id
 * @property {String} name
 * @property {Number} score
 * @property {String} api
 * @property {Event[]} events - List of all event IDs
 */

/**
 * Object representing an Event
 * @typedef {Object} Event
 * @property {String} id
 * @property {String} player_id
 * @property {String} query
 * @property {Number} difficulty - "0" for warmup, 1 for round 1, etc.
 * @property {Number} points_gained - +ve / -ve point difference
 * @property {NO_RESPONSE/WRONG/CORRECT} response_type 
 * @property {RFC3339} timestamp
 */

/**
 * Object representing a Game
 * @typedef {Object} Game
 * @property {String} id
 * @property {Number} round
 * @property {player_id[]} players - List of player IDs
 * @property {Boolean} paused
 */

// Main page requests - ("/api")

/**
 * Fetches all games
 * @return {{gameId: Game, ...}} Object containing all game objects
 */
export async function fetchAllGames() {
  try {
    const response = await instance.get(homeAPI())
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Creates a new game and returns its game json object
 * @return {Game} Game object of newly created game
 */
export async function createNewGame() {
  try {
    const response = await instance.post(homeAPI())
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Drops all games, ids, events
 * @return TODO
 */
export async function deleteEverything() {
  try {
    const response = await instance.delete(homeAPI())
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// Requests to ("/api/(gameId)")

/**
 * Fetches game json object for a given game ID
 * @param  {String} gameId
 * @return {Game} Game json object
 */
export async function fetchGame(gameId) {
  try {
    const response = await instance.get(gameAPI(gameId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Updates game by either updating the round, or by pausing/unpausing the game
 * 
 * Sending an object containing {"round": roundNumber} will advance the game to roundNumber
 * Sending an object containing {"pause": true/false} will pause the game if true and unpause if false
 * @param  {String} gameId 
 * @param  {{"round": Number, "pause": Boolean}} data Object containing either the round to advance to or whether to pause/unpause the game
 * @return {String} 
 */
export async function updateGame(gameId, data) {
  try {
    const response = await instance.put(gameAPI(gameId, data))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Drops a given game
 * @param  {String} gameId 
 * @return {{"deleted": gameId}} ID of deleted game
 */
export async function deleteGame(gameId) {
  try {
    const response = await instance.delete(gameAPI(gameId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// Requests to ("/api/(game_id)/players")

/**
 * Fetches all players in a given game
 * @param  {String} gameId 
 * @return {{"players": Player[]}} Object containing list of all players
 */
export async function fetchPlayers(gameId) {
  try {
    const response = await instance.get(playersAPI(gameId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Validates user submission and creates new player if valid (returns false if invalid)
 * @param  {String} gameId 
 * @param  {String} name   Name submitted by user
 * @param  {String} api    URL submitted by user
 * @return {Player}   player json object for newly created player
 */
export async function createPlayer(gameId, name, api) {

  const valid = await validateData(gameId, { name: name, api: api })

  if (!valid) {
    console.error("Invalid data submitted")
    return false
  }

  const playerData = {
    name: name.trim(),
    api: api
  }

  try {
    const response = await instance.post(playersAPI(gameId), playerData)
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// Helper function for createPlayer()
async function validateData(gameId, data) {

  // Check gameId exists
  try {
    const response = await fetchGame(gameId)
    console.log(response)
  } catch (error) {
    showFailureNotification("Error creating player", "Game id does not exist!")
    return false
  }

  const players = await fetchPlayers(gameId)

  if (data.name) {
    const name = data.name.trim()

    // Check player name is not empty
    if (name === "") {
      showFailureNotification("Error creating player", "Your name cannot be empty!")
      return false
    }

    // Check player name is unique in a game
    if (name in players) {
      showFailureNotification("Error creating player", "Your name already exists in the game!")
      return false
    }
  }

  if (data.api) {
    // Check valid URL
    if (data.api.substring(0, 7) !== "http://" && data.api.substring(0, 8) !== "https://") {
      showFailureNotification("Error creating player", "You entered an invalid URL!")
      return false
    }

    const apis = players.map((player) => { player.api })

    if (data.api in apis) {
      showFailureNotification("Error creating player", "Your url already exists in the game!")
      return false
    }
  }

  return true
}

/**
 * Deletes all players in a game
 * @param  {String} gameId 
 * @return TODO
 */
export async function deleteAllPlayers(gameId) {
  try {
    const response = await instance.delete(playersAPI(gameId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// ("/api/(game_id)/players/(player_id")

/**
 * Returns player json object for a given player in a given game
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @return {Player} Player json object
 */
export async function fetchPlayer(gameId, playerId) {
  try {
    const response = await instance.get(playerAPI(gameId, playerId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Updates a player's name and/or api url
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @param  {{name: String, api: String}} data Object containing new name and/or new api
 * @return {Player} Updated player json object
 */
export async function updatePlayer(gameId, playerId, data) {

  const valid = await validateData(gameId, data)

  if (!valid) {
    console.error("Invalid data submitted")
    return false
  }

  try {
    const response = await instance.put(playerAPI(gameId, playerId), data)
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Drops a player
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @return {{"deleted": playerId}} ID of the deleted player
 */
export async function deletePlayer(gameId, playerId) {
  try {
    const response = await instance.delete(playerAPI(gameId, playerId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// "/api/(game_id)/players/(player_id)/events"

/**
 * Returns a list of all event json objects for a given player
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @return {{"events": Event[]}} List of all event json objects
 */
export async function fetchAllEvents(gameId, playerId) {
  try {
    const response = await instance.get(playerEventsAPI(gameId, playerId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Deletes all events for a given player
 * @param {String} gameId 
 * @param {String} playerId 
 * @return TODO
 */
export async function deleteAllEvents(gameId, playerId) {
  try {
    const response = await instance.delete(playerEventsAPI(gameId, playerId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

// "/api/(game_id)/players/(player_id)/events/(event_id)"

/**
 * Returns the event json object for a given eventId
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @param  {String} eventId 
 * @return {Event} Event json object
 */
export async function fetchEvent(gameId, playerId, eventId) {
  try {
    const response = await instance.get(eventAPI(gameId, playerId, eventId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}

/**
 * Drops a given event
 * @param  {String} gameId 
 * @param  {String} playerId 
 * @param  {String} eventId 
 * @return {"deleted": eventId} ID of deleted event
 */
export async function deleteEvent(gameId, playerId, eventId) {
  try {
    const response = await instance.delete(eventAPI(gameId, playerId, eventId))
    return response.data
  } catch (error) {
    alertError(error)
  }
}


// import { gameCreationUrl, gameUrl, playerCreationUrl } from '../utils/urls';
// import { alertError } from '../utils/utils'
// import axios from 'axios';
//
// export function justJsonHeaders() {
//   return {
//     headers: {
//       'Content-Type': 'application/json',
//     }
//   }
// }

// export function requestGameCreation() {
//   return axios
//     .post(gameCreationUrl(), {}, justJsonHeaders())
//     .then(request => {
//       console.log(request)
//       return {
//         id: request.data.id
//       }
//     })
//     .catch(alertError)
// }

// export function validPlayerData(gameId, name, url) {
//   let player = name.trim()

//   if (player === "")
//     return 2

//   try {
//     const response = axios.get(gameUrl(gameId))
//     console.log(response)
//   }
//   catch (err) {
//     alertError(err)
//     return 1
//   }

//   let players = getPlayersFromGameId(gameId)

//   if (player in players)
//     return 3

//   if (url.substring(0, 7) === "http://" || url.substring(0, 8) === "https://")
//     return 0

//   return 4
// }

// export function playerCreationData(name, api) {
//   return {
//     name: name.trim(),
//     api: api
//   }
// }

// export function requestPlayerCreation(gameId, playerData) {
//   return axios
//     .post(playerCreationUrl(gameId), playerData, justJsonHeaders())
//     .then(request => {
//       console.log(request)
//       return request.data
//     })
//     .catch(alertError)
// }

// export function getPlayersFromGameId(gameId) {
//   let url = playerCreationUrl(gameId)
//   axios.get(url)
//     .then(data => { return data.players })
//     .catch(err => alertError("Error fetching players from game id: " + err.response.data))
//   return []
// }

// const fetchEvents = async () => {
//   try {
//     const response = await axios.get("/api" + playerPageUrl(params.gameid, params.id));
//     return response;
//   } catch (error) {
//     // console.error(error);
//   }
// }


// const deletePlayer = (id) => {
//   console.log("deleted player", id);
// };
