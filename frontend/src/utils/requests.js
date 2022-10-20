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
export async function requestGameCreation() {
  return await axios
    .post(gameCreationUrl(), null, justJsonHeaders())
    .then(game => {
      return {
        wasCreated: true,
        id: game.id
      }
    })
    .catch(error => {
      alertError(error)
      return {
        wasCreated: false
      }
    })
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

export async function requestPlayerCreation(gameId, playerData) {
  return await axios
    .post(playerCreationUrl(), playerData, justJsonHeaders())
    .then(player => {
      return {
        wasCreated: true,
        player: player
      }
    })
    .catch(error => {
      alertError(error)
      return {
        wasCreated: false
      }
    })
}
