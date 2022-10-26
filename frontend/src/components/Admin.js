import React, { useEffect, useState, useCallback } from "react"
import { useParams } from "react-router-dom"
import { Button, Container } from "@mantine/core"

import { fetchGame, updateGame } from "../utils/requests"

import "../styles/Admin.css"

function Admin() {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)

  const params = useParams()

  // Fetches game data (current round and number of players)
  const getGameData = useCallback(async () => {
    try {
      console.log(params.gameId)
      const response = await fetchGame(params.gameId)
      setRound(response.round)
      setPlayerNo(response.players.length)
    } catch (error) {
      // TODO
    }
  }, [params.gameId])

  // Fetches game data every 2 seconds
  useEffect(() => {
    const timer = setInterval(getGameData, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [getGameData])

  // Increments round
  const advanceRound = async () => {
    try {
      await updateGame(params.gameId, { round: round + 1 })
      setRound(round + 1);
    } catch (error) {
      // TODO
    }
  };

  return (
    <Container size="xl" px="xs">
      <h3>Game ID</h3>
      <h4 className="bar">{params.gameId}</h4>
      <br />
      <h3>Number of Players</h3>
      <h4 className="bar">{playerNo}</h4>
      <br />
      <div className="rounds-bar">
        <div>
          <h3>Rounds</h3>
        </div>
        <Button
          variant="outline"
          color="dark"
          radius="md"
          size="md"
          style={{
            marginLeft: "20px",
          }}
          onClick={() => advanceRound()}
        >
          Advance Round
        </Button>
      </div>
      <h4 className="bar">{round === 0 ? "Warmup" : round}</h4>
    </Container>
  );
}

export default Admin;
