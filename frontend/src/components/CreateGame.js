import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';

function CreateGame(setOpened) {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  const addPlayer = (e) => {
    e.preventDefault();

    if (name.trim() === "") {
      showNotification({  
        title: "Error creating player",
        message: "You forgot to enter a name!",
        icon: <IconX size={18} />, 
        color: "red"
      });

      return
    }

    const playerObject = {
      name: name.trim(),
      url: url.trim(),
    };

    axios
      .post("https://extreme-restartup.fly.dev/players", playerObject)
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
        {/* <form method="post" action="https://extreme-restartup.fly.dev/players">
            <label htmlFor="name">Name: </label>
            <input type="text" id="name" name="name"/>

            <label htmlFor="url">URL: </label>
            <input type="text" id="url" name="url" placeholder="http://...."/>

            <input type="submit" value="Submit" />
        </form> */}
        
        <form onSubmit={addPlayer}>
          <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required/>
          <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required/>
          <Button type="submit">Submit</Button>
        </form>
    </div>
  )
}

export default CreateGame