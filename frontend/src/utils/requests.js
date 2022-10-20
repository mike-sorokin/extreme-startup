import { gameCreationUrl, playerCreationUrl } from '../utils/urls';
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

/*
  todo
  pre: validation done outside
*/
export function playerCreationData(name, api) {
  return {
    name: name,
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
