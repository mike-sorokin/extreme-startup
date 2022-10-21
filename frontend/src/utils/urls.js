import { alertError } from "./utils"
import axios from 'axios';

const API_URL_PREFIX = "/api"
const rootUrl = () => API_URL_PREFIX

export function gameCreationUrl() {
  return rootUrl()
}

export function gameUrl(gameId) {
  return `${rootUrl()}/${gameId}`
}

export function getPlayersFromGameId(gameId) {
  let url = playerCreationUrl(gameId)
  axios.get(url)
  .then(data => {return data.players})
  .catch(err => alertError("Error fetching players from game id: " + err.response.data))
  return []
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
