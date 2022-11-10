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
      console.log(response)
      showSuccessNotification('Successfully Created Player!')
      navigate(playerUrl(response.game_id, response.id))
    } catch (error) {
      // TODO
    }
  }

  // Adds a new moderator to the game
  const submitModerator = async (event) => {
    event.preventDefault()

    try {
      const response = await createModerator(gameId, { password: pwd })
      console.log(response)

      if (response.valid) {
        showSuccessNotification('Successfully Joined as Moderator!')
        navigate(adminUrl(gameId))
      } else {
        showFailureNotification('Error creating moderator', 'Game password incorrect!')
      }
    } catch (error) {
      // TODO
    }
  }

  return (
    <div>
      <Switch
        label="Join as Moderator"
        size="md"
        color="teal"
        checked={mod} onChange={(e) => setMod(e.currentTarget.checked)}
      />
      <Space h="md" />
      {
        mod
          ? <form onSubmit={submitModerator}>
          <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abcd1234)" label="Enter game id:" required />
          <Space h="md" />
          <PasswordInput value={pwd} onChange={(e) => setPwd(e.target.value)} placeholder="Game password" label="Enter game password:" required />
          <Space h="md" />
          <Button variant="outline" color="grape" type="submit">Join as Moderator!</Button>
        </form>
          : <form onSubmit={submitPlayer}>
          <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abcd1234)" label="Enter game id:" required />
          <Space h="md" />
          <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
          <Space h="md" />
          <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
          <Space h="md" />
          <Button variant="outline" color="green" type="submit">Join!</Button>
        </form>
      }
    </div>
  )
}

export default AddPlayer
