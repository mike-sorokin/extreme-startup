import { requestPlayerCreation, playerCreationData } from '../utils/requests'
import { showSuccessfulNotification } from '../utils/utils'
import { playerPageUrl } from '../utils/urls'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom'


function AddPlayer(setOpened) {
  const [gameId, setGameId] = useState("");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  const navigate = useNavigate();

  const submission = event => {
    event.preventDefault()
    const playerData = playerCreationData(name, url)
    return requestPlayerCreation(gameId, playerData)
      .then(player => {
        showSuccessfulNotification("Successfully Created Player")
        navigate(playerPageUrl(player.game_id, player.id))
      })
  }

  return (
    <div>
      <form onSubmit={submission}>
        <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abc123)" label="Enter game id:" required />
        <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
        <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
        <Button type="submit">Submit</Button>
      </form>
    </div>
  )
}

export default AddPlayer
