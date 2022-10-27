import { React, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Container, Table, Badge } from "@mantine/core";

import { fetchPlayer } from "../utils/requests";

import PlayerTable from "./PlayerTable";

function Player() {
  const [playerData, setPlayerData] = useState({})

  const params = useParams();

  // Fetches player json object from backend
  useEffect(() => {
    const getPlayerData = async () => {
      try {
        const response = await fetchPlayer(params.gameId, params.id)
        console.log("response", response)
        setPlayerData(response)
      } catch (error) {
        // TODO
      }
    }

    getPlayerData()
  }, [params.gameId, params.id]);

  return (
    <Container size="xl" px="xs">
      <br />
      <h3>Player ID</h3>
      <h4 style={{ color: 'grey' }}>{playerData.id}</h4>
      <br />
      <h3>Game ID</h3>
      <h4 style={{ color: 'grey' }}>{playerData.game_id}</h4>
      <br />
      <h3>Name</h3>
      <h4 style={{ color: 'grey' }}>{playerData.name}</h4>
      <br />
      <h3>API</h3>
      <h4 style={{ color: 'grey' }}>{playerData.api}</h4>
      <br />
      <h3>Score</h3>
      <h4 style={{ color: 'grey' }}>{playerData.score}</h4>
      <br />
      <h3>Events</h3>
      <PlayerTable events={playerData.events} />
    </Container>
  );
}

export default Player;
