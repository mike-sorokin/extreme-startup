import { gameCreationUrl, gameUrl, getPlayersFromGameId, playerCreationUrl } from '../utils/urls';
import { alertError } from '../utils/utils'
import axios from 'axios';

export function justJsonHeaders() {
  return {
    headers: {
      'Content-Type': 'application/json',
    }
  }
}

/*
  todo doc
*/
export function requestGameCreation() {
  return axios
    .post(gameCreationUrl(), {}, justJsonHeaders())
    .then(request => {
      console.log(request)
      return {
        id: request.data.id
      }
    })
    .catch(alertError)
}

export function validPlayerData(gameId, name, url) {
  let player = name.trim()

  if (player === "")
    return 2

  try {
    const response = axios.get(gameUrl(gameId))
    console.log(response)
  }
  catch (err) {
    alertError(err)
    return 1
  }

  let players = getPlayersFromGameId(gameId)

  if (player in players)
    return 3

  if (url.substring(0, 7) === "http://" || url.substring(0, 8) === "https://")
    return 0

  return 4
}

export function playerCreationData(name, api) {
  return {
    name: name.trim(),
    api: api
  }
}

export function requestPlayerCreation(gameId, playerData) {
  return axios
    .post(playerCreationUrl(gameId), playerData, justJsonHeaders())
    .then(request => {
      console.log(request)
      return request.data
    })
    .catch(alertError)
}
