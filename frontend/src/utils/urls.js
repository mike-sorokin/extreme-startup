const API_URL_PREFIX = "/api"
const rootUrl = () => API_URL_PREFIX

export function gameCreationUrl() {
  return rootUrl()
}

export function gameUrl(gameId) {
  return `${rootUrl()}/${gameId}`
}

export function playerCreationUrl(gameId) {
  return `${gameUrl(gameId)}/players`
}

export function gamePageUrl(gameId) {
  return `/${gameId}`
}

export function playerPageUrl(gameId, playerId) {
  return `${gamePageUrl(gameId)}/players/${playerId}`
}
