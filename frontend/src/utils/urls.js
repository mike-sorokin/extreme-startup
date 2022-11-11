/**
 * URLs for navigation (not prepended with "/api")
 */
export function homeUrl () {
  return '/'
}

export function gameUrl (gameId) {
  return `/${gameId}`
}

export function playersUrl (gameId) {
  return `/${gameId}/players`
}

export function playerUrl (gameId, playerId) {
  return `/${gameId}/players/${playerId}`
}

export function adminUrl (gameId) {
  return `/${gameId}/admin`
}

export function gameReviewUrl (gameId) {
  return `/review/${gameId}`
}

/**
 * URLs for requests
 */
const API_PREFIX = '/api'

// Management of all games
export function homeAPI () {
  return `${API_PREFIX}`
}

// Management of a specific game
export function gameAPI (gameId) {
  return `${API_PREFIX}/${gameId}`
}

// Management of authentication in a game
export function authAPI (gameId) {
  return `${API_PREFIX}/${gameId}/auth`
}

// Management of all players in a game
export function scoresAPI (gameId) {
  return `${API_PREFIX}/${gameId}/scores`
}

// Management of all players in a game
export function playersAPI (gameId) {
  return `${API_PREFIX}/${gameId}/players`
}

// Management of a specific player in a game
export function playerAPI (gameId, playerId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}`
}

// Management of events for a specific player
export function playerEventsAPI (gameId, playerId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}/events`
}

// Management of a specific event for a player
export function eventAPI (gameId, playerId, eventId) {
  return `${API_PREFIX}/${gameId}/players/${playerId}/events/${eventId}`
}

// Management of a specific event for a player
export function gameoverAPI (gameId) {
  return `${API_PREFIX}/${gameId}/gameover`
}
