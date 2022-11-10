import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Space, Switch, PasswordInput, TextInput } from '@mantine/core'

import { createPlayer, createModerator } from '../utils/requests'
import { adminUrl, playerUrl } from '../utils/urls'
import { showFailureNotification, showSuccessNotification } from '../utils/utils'

function AddPlayer () {
  const [mod, setMod] = useState(false)
  const [pwd, setPwd] = useState('')
  const [gameId, setGameId] = useState('')
  const [name, setName] = useState('')
  const [url, setUrl] = useState('')

  const navigate = useNavigate()

  // Adds a new player to the game
  const submitPlayer = async (event) => {
    event.preventDefault()

    try {
      const response = await createPlayer(gameId, name, url)
      showSuccessNotification('Successfully Created Player!')
      navigate(playerUrl(response.game_id, response.id))
    } catch (error) {
      // Notification has already been shown, currently all errors have already been handled
    }
  }

  // Adds a new moderator to the game
  const submitModerator = async (event) => {
    event.preventDefault()

    try {
      const response = await createModerator(gameId, { password: pwd })

      if (response.valid) {
        showSuccessNotification('Successfully Joined as Moderator!')
        navigate(adminUrl(gameId))
      } else {
        showFailureNotification('Error creating moderator', 'Game password incorrect!')
      }
    } catch (error) {
      if (error.response.status === 406) {
        console.error('password not sent in request')
      }
    }
  }

  return (
    <div>
      <Switch
        label="Join as Moderator"
        size="md"
        color="teal"
        checked={mod} onChange={(e) => setMod(e.currentTarget.checked)}
        data-cy="moderator-toggle"
      />
      <Space h="md"></Space>
      {
        mod
          ? <form onSubmit={submitModerator}>
          <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abcd1234)" label="Enter game id:" required data-cy="mod-game-id-input"/>
          <Space h="md"></Space>
          <PasswordInput value={pwd} onChange={(e) => setPwd(e.target.value)} placeholder="Game password" label="Enter game password:" required data-cy="mod-pwd-input" />
          <Space h="md"></Space>
          <Button variant="outline" color="grape" type="submit">Join as Moderator!</Button>
        </form>
          : <form onSubmit={submitPlayer}>
          <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abcd1234)" label="Enter game id:" required data-cy="game-id-input" />
          <Space h="md"></Space>
          <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required data-cy="player-name-input"/>
          <Space h="md"></Space>
          <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required data-cy="url-input"/>
          <Space h="md"></Space>
          <Button variant="outline" color="green" type="submit">Join!</Button>
        </form>
      }
    </div>
  )
}

export default AddPlayer
