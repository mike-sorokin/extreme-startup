import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Button, Container } from '@mantine/core'

import { fetchGame, updateGame } from '../utils/requests'

import '../styles/Admin.css'
import { Button, Card, Container, Space, Title } from '@mantine/core'
import axios from 'axios'
import { gameAPI } from '../utils/urls'

function Admin () {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)
  const [gamePaused, setGamePaused] = useState(false)

  const params = useParams()

  // Fetches game data every 2 seconds (current round and number of players)
  useEffect(() => {
    const getGameData = async () => {
      try {
        const response = await fetchGame(params.gameId)
        setRound(response.round)
        setPlayerNo(response.players.length)
      } catch (error) {
        // TODO
      }
    }

    const timer = setInterval(getGameData, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId])

  // Increments round
  const advanceRound = async () => {
    try {
      await updateGame(params.gameId, { round: round + 1 })
      setRound(round + 1)
    } catch (error) {
      // TODO
    }
  }

  // Send a {"pause": ""} request to unpause, {"pause": "p"} to pause
  const togglePauseRound = async () => {
    try {
      const response = await updateGame(params.gameId, { pause: (gamePaused ? '' : 'p') })
      console.log(response)
      setGamePaused(response === 'GAME_PAUSED')
    } catch (error) {
      // TODO
    }
  function togglePauseButton (color, text) {
    return <Button variant="outline"
      color={color}
      radius="md"
      size="md"
      style={{
        marginLeft: '20px'
      }}
      onClick={() => togglePauseRound()}>
      {text}
    </Button>
  }

  const roundsBarStyle = {
    width: '100%',
    display: 'inline-flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center'
  }

  return (
    <Container size="xl" px="xs">
      <Title order={1} color="white" weight={1000}>Host Page</Title>
      <Space h="md" />
      <Card shadow="sm" p="lg" radius="md" withBorder>
        <h3>Game ID</h3>
        <h4 style={{ color: 'grey' }}>{params.gameId}</h4>
        <br />
        <h3>Number of Players</h3>
        <h4 style={{ color: 'grey' }}>{playerNo}</h4>
        <br />
        <div style={roundsBarStyle}>
          <div>
            <h3>Rounds</h3>
          </div>
          <Button variant="outline"
            color="indigo"
            radius="md"
            size="md"
            style={{
              marginLeft: '20px'
            }}
            onClick={() => advanceRound()}>
            Advance Round
          </Button>
          { gamePaused
            ? togglePauseButton('green', 'Resume')
            : togglePauseButton('yellow', 'Pause')
          }
        </div>
        {<h4 style={{ color: 'grey' }}>{gamePaused ? 'PAUSED' : round}</h4>}
      </Card>
    </Container>
  )
}

export default Admin
