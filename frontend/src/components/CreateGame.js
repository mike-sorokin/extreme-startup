import { gamePageUrl } from '../utils/urls'
import { requestGameCreation, requestPlayerCreation, playerCreationData } from '../utils/requests'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';
import { useNavigate } from 'react-router-dom'


// TODO: Create a game! This code currently is just a duplicate of AddPlayer
// UPDATE: it is in progress

function CreateGame(setOpened) {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  const navigate = useNavigate();

  const submission = event => {
    event.preventDefault()
    return requestGameCreation()
      .then(game => {
        const playerData = playerCreationData(name, url)
        return requestPlayerCreation(game.id, playerData)
      })
      .then(player => {
        // setOpened(false)
        navigate(gamePageUrl(player.game_id))
      })
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
