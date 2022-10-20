import { alertError } from '../utils/utils'
import { gameCreationUrl, playerCreationUrl, playerPageUrl } from '../utils/urls'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';
import { Navigate } from 'react-router-dom';

// TODO: Create a game! This code currently is just a duplicate of AddPlayer
/*
  todo doc
*/
function requestGameCreation() {
  const resultGame = {
    wasCreated: false,
    id: null
  }
  axios.post(gameCreationUrl())
    .then(game => {
      resultGame.wasCreated = true
      resultGame.id = game.id
    })
    .catch(alertError)
  return resultGame
}

/*
  todo
  pre: validation done outside
*/
function playerCreationData(name, api) {
  return {
    name: name,
    api: api
  }
}

function requestPlayerCreation(gameId, playerData) {
  const resultPlayerWrapper = {
    wasCreated: false,
    player: null
  }
  axios.post(playerCreationUrl(), playerData)
    .then(player => {
      resultPlayerWrapper.wasCreated = true
      resultPlayerWrapper.player = player
    })
    .catch(alertError)
  return resultPlayerWrapper
}

function CreateGame(setOpened) {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  // const addPlayer = (e) => {
  //   e.preventDefault();
  //
  //   if (name.trim() === "") {
  //     showNotification({
  //       title: "Error creating player",
  //       message: "You forgot to enter a name!",
  //       icon: <IconX size={18} />,
  //       color: "red"
  //     });
  //
  //     return
  //   }
  //
  //   const playerObject = {
  //     name: name.trim(),
  //     url: url.trim(),
  //   };
  //
  //   axios
  //     .post("/api/players", playerObject)
  //     .then(() => {
  //       showNotification({
  //         title: "Success",
  //         message: "Player successfully created!",
  //         icon: <IconCheck size={18} />,
  //         color: "teal"
  //       });
  //     })
  //     .catch((err) => alert(err.response.data));
  //   setOpened(false)
  //
  //   // TODO: Get player id from backend and redirect to player page
  // };

  const submission = event => {
    event.preventDefault()
    const game = requestGameCreation()
    if (!game.wasCreated) {
      return
    }
    const playerData = playerCreationData(name, url)
    const playerWrapper = requestPlayerCreation(game.id, playerData)
    if (!playerWrapper.wasCreated) {
      return
    }
    setOpened(false)
    const player = playerData.player
    return (<Navigate to={playerPageUrl(game.id, player.id)} />)
  }

  return (
    <div>
      <form onSubmit={submission}>
        <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
        <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
        <Button type="submit">Submit</Button>
      </form>
    </div>
  )
}

export default CreateGame
