import { requestPlayerCreation, playerCreationData } from '../utils/requests'
import { showSuccessfulNotification } from '../utils/utils'
import { playerPageUrl } from '../utils/urls'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom'


function AddPlayer(setOpened) {

  const navigate = useNavigate();

    let gameId = id.trim()
    let playerName = name.trim()
    let playerUrl = url.trim()

    if (gameId === "") {
      showNotification({
        title: "Error creating player",
        message: "You forgot to enter a game id!",
        icon: <IconX size={18} />,
        color: "red"
      });

      return
    }

    if (playerName === "") {
      showNotification({
        title: "Error creating player",
        message: "You forgot to enter a name!",
        icon: <IconX size={18} />,
        color: "red"
      });

      return
    }

    const playerObject = {
      name: playerName,
      url: playerUrl,
    };

    const json = "/api/" + gameId + "/players";

    axios
      .post(json, playerObject)
      .then(() => {
        showNotification({
          title: "Success",
          message: "Player successfully created!",
          icon: <IconCheck size={18} />,
          color: "teal"
        });
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
