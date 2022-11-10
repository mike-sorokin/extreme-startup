import { showNotification } from '@mantine/notifications'
import { IconCheck, IconX, IconAlertTriangle } from '@tabler/icons'
import { React } from 'react'

import { checkAuth } from '../utils/requests'

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

export function playersAsArray (playersDict) {
  const arr = []
  for (const playerId in playersDict) {
    arr.push(playersDict[playerId])
  }
  return arr
}

export async function updateSessionData (gameId, setIsAdmin, setPlayerID) {
  const auth = await checkAuth(gameId)
  const admin = auth.authorized
  const player = auth.player

  setIsAdmin(admin)
  setPlayerID(player)
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
