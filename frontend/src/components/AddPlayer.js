import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';

function AddPlayer(setOpened) {
  const [id, setId] = useState("");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  const addPlayer = (e) => {
    e.preventDefault();

    gameId = id.trim()
    playerName = name.trim()
    playerUrl = url.trim()

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
      .catch((err) => alert(err.response.data));

    setOpened(false)

    // TODO: Get player id from backend and redirect to player page
  };

  return (
    <div>
      <form onSubmit={addPlayer}>
        <TextInput value={id} onChange={(e) => setId(e.target.value)} placeholder="Game id (e.g. abc123)" label="Enter game id:" required />
        <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
        <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
        <Button type="submit">Submit</Button>
      </form>
    </div>
  )
}

export default AddPlayer