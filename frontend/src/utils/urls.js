import { alertError } from "./utils"
import axios from 'axios';

/**
 * URLs for navigation (not prepended with "/api")
 */
export function home() {
  return "/"
}

export function game(gameId) {
  return `/${gameId}`
}

export function players(gameId) {
  return `/${gameId}/players`
}

export function player(gameId, playerId) {
  return `/${gameId}/players/${playerId}`
}

export function admin(gameId) {
  return `/${gameId}/admin`
}

/**
 * URLs for requests
 */
const API_PREFIX = "/api"

// Management of all games
export function homeAPI() {
  return `${API_PREFIX}`
}

// Management of a specific game
export function gameAPI(gameId) {
  return `${API_PREFIX}/${gameId}`
}

// Management of all players in a game
export function playersAPI(gameId) {
  return `${API_PREFIX}/${gameId}/players`
}

// Management of a specific player in a game
export function playerAPI(gameId, playerId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}`
}

// Management of events for a specific player
export function playerEventsAPI(gameId, playerId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}/events`
}

// Management of a specific event for a player
export function eventAPI(gameId, playerId, eventId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}/events/${eventId}`
}


// const API_PREFIX = "/api"
// const rootUrl = () => API_PREFIX
// export function gameCreationUrl() {
//   return API_PREFIX
// }

// export function gameUrl(gameId) {
//   return `${rootUrl()}/${gameId}`
// }

// export function playerCreationUrl(gameId) {
//   return `${gameUrl(gameId)}/players`
// }

// export function gamePageUrl(gameId) {
//   return `/${gameId}`
// }

// export function playerPageUrl(gameId, playerId) {
//   return `${gamePageUrl(gameId)}/players/${playerId}`
// }
