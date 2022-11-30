import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@mantine/core'
import { showNotification, updateNotification } from '@mantine/notifications'
import { IconCheck, IconHome, IconX, IconAlertTriangle, IconInfoCircle } from '@tabler/icons'
import { homeUrl } from './urls'

export function str (obj) {
  return JSON.stringify(obj)
}

export function alertError (error) {
  console.error(error)
  throw error
}

export default function HomeButton ({ size }) {
  const navigate = useNavigate()
  return (
    <Button variant="outline" color="yellow" radius="md" size={size}
      leftIcon={<IconHome />} onClick={() => navigate(homeUrl())}>
      Go to Home Page
    </Button>
  )
}

export function showLoadingNotification (notifId, header, msg) {
  showNotification({
    id: notifId,
    title: header,
    message: msg,
    color: 'teal',
    loading: true
  })
}

export function updateLoadingNotification (notifId, header, msg) {
  updateNotification({
    id: notifId,
    title: header,
    message: msg,
    icon: <IconCheck size={18} />,
    color: 'teal'
  })
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

export function showInfoNotification (header, msg) {
  showNotification({
    title: header,
    message: msg,
    icon: <IconInfoCircle size={18} />,
    color: 'blue'
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
 * If playerID is empty, (i.e. when player is a spectator) this function does nothing
 * Note that the sort is not inplace. The array is copied and returned new.
 * @return {Player[]} Object containing all players objects of a game, ordered by
 * inital order, but the current player in a session is on top of a list
 */
export function withCurrentPlayerLiftedIfPresent (playerID, players) {
  if (playerID === '') {
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
