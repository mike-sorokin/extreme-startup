import { showNotification } from '@mantine/notifications'
import { IconCheck, IconX, IconAlertTriangle } from '@tabler/icons'
import { React } from 'react'

export function str (obj) {
  return JSON.stringify(obj)
}

export function alertError (error) {
  console.log(error.toJSON())
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
