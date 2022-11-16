import { showNotification } from '@mantine/notifications'
import { IconCheck, IconX, IconAlertTriangle, IconInfoSquare } from '@tabler/icons'
import { React } from 'react'

export function str (obj) {
  return JSON.stringify(obj)
}

export function alertError (error) {
  console.error(error)
  throw error
}

export function showSuccessNotification (msg) {
  showNotification({
    title: 'Success',
    message: msg,
    icon: <IconCheck size={18} />,
    color: 'teal'
  })
}

export function showFailureNotification (header, msg) {
  showNotification({
    title: header,
    message: msg,
    icon: <IconX size={18} />,
    color: 'red'
  })
}

export function showErrorNotification (header, msg) {
  showNotification({
    title: header,
    message: msg,
    icon: <IconAlertTriangle size={18} />,
    color: 'yellow'
  })
}

export function showGeneralNotification (header, msg) {
  showNotification({
    title: header,
    message: msg,
    icon: <IconInfoSquare size={18} />,
    color: 'indigo'
  })
}

export function playersAsArray (playersDict) {
  const arr = []
  for (const playerId in playersDict) {
    arr.push(playersDict[playerId])
  }
  return arr
}

/**
 * Creates array where the current player is lifted on top.
 * Note that the sort is not inplace. The array is copied and returned new.
 * @return {Player[]} Object containing all players objects of a game, ordered by
 * inital order, but the current player in a session is on top of a list
 */
export function withCurrentPlayerLiftedIfPresent (playerID, players) {
  console.log('playerID')
  console.log(playerID)
  if (playerID === '') {
    console.log('playerID is empty ')
    return players
  }
  return players.sort((p1, p2) => p1.id === playerID ? -1 : p2.id === playerID ? 1 : 0)
}

export class HTTPError extends Error {
  constructor (message, status) {
    super(message)
    this.response = {
      status
    }
  }

  toJSON () {
    return { message: this.message, response: { status: this.response.status } }
  }
}
