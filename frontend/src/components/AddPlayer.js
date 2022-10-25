import React from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextInput, Button } from "@mantine/core";

import { createPlayer } from "../utils/requests";
import { player } from "../utils/urls";
import { showSuccessNotification } from "../utils/utils";

// Do we need this setOpened prop?
function AddPlayer(setOpened) {
  const [gameId, setGameId] = useState("");
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await createPlayer(gameId, name, url);
      showSuccessNotification("Successfully Created Player!");
      navigate(player(response.game_id, response.id));
    } catch (error) {
      // TODO
    }

    // let validStatus = validPlayerData(gameId, name, url);

    // if (validStatus === 0) {
    //   const playerData = playerCreationData(name, url);
    //   return requestPlayerCreation(gameId, playerData).then((player) => {
    //     showSuccessfulNotification("Successfully Created Player!");
    //     console.log("player");
    //     console.log(player);
    //     navigate(playerPageUrl(player.game_id, player.id));
    //   });
    // }

    // if (validStatus === 1) {
    //   showFailureNotification("Error creating player", "Game id does not exist!");
    // } else if (validStatus === 2) {
    //   showFailureNotification("Error creating player", "Your name cannot be empty!");
    // } else if (validStatus === 3) {
    //   showFailureNotification("Error creating player", "Your name already exists in the game!");
    // } else {
    //   showFailureNotification("Error creating player", "You entered an invalid URL!");
    // }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <TextInput value={gameId} onChange={(e) => setGameId(e.target.value)} placeholder="Game id (e.g. abc123)" label="Enter game id:" required />
        <TextInput value={name} onChange={(e) => setName(e.target.value)} placeholder="Your player name" label="Enter player name:" required />
        <TextInput value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Your URL (http://...)" label="Enter URL:" required />
        <Button type="submit">Submit</Button>
      </form>
    </div>
  );
}

export default AddPlayer;
