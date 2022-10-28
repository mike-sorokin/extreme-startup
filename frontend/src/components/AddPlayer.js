import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Space, TextInput } from '@mantine/core'

import { createPlayer } from '../utils/requests'
import { playerUrl } from '../utils/urls'
import { showSuccessNotification } from '../utils/utils'

function AddPlayer () {
  const [gameId, setGameId] = useState('')
  const [name, setName] = useState('')
  const [url, setUrl] = useState('')

  const navigate = useNavigate()

  // Adds a new player to the game
  const handleSubmit = async (event) => {
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

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abcd1234)" label="Enter game id:" required />
        <Space h="md"></Space>
        <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
        <Space h="md"></Space>
        <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
        <Space h="md"></Space>
        <Button type="submit">Submit</Button>
      </form>
    </div>
  )
}

export default AddPlayer
