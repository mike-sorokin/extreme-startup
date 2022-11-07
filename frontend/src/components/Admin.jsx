import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Badge, Button, Card, Container, Space, Title } from '@mantine/core'
import { useClipboard } from '@mantine/hooks'

import { fetchGame, updateGame } from '../utils/requests'

function Admin () {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)
  const [gamePaused, setGamePaused] = useState(false)
  // const [isAdmin, setIsAdmin] = useState(false)

  const params = useParams()
  const clipboard = useClipboard({ timeout: 500 })

  // const updateSessionData = async () => {
  //   const admin = await checkAuth(params.gameId)
  //   setIsAdmin(admin)
  //   console.log(isAdmin)
  // }

  // updateSessionData()

  // Fetches game data every 2 seconds (current round and number of players)
  useEffect(() => {
    const getGameData = async () => {
      try {
        const response = await fetchGame(params.gameId)
        setRound(response.round)
        setGamePaused(response.paused)
        setPlayerNo(response.players.length)
      } catch (error) {
        // TODO
      }
    }

    getGameData()
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
  }

  function togglePauseButton (color, text) {
    return <Button compact variant="outline"
      color={color}
      radius="md"
      size="md"
      style={{ marginLeft: '10%', width: '110px' }}
      onClick={() => togglePauseRound()}>
      {text}
    </Button>
  }

  function roundBadge (color, text) {
    return <Badge size="xl" color={color} variant="filled"
      style={{ width: '200px' }}>
      {text}
    </Badge>
  }

  return (
    <Container size="xl" px="xs">
      <Title order={1} color="white" weight={1000}>Admin Page</Title>
      <Space h="md" />
      <Card shadow="sm" p="lg" radius="md" withBorder>
        <h3>Game ID</h3>
        <div style={{ display: 'inline-flex', flexDirection: 'row' }}>
          <Title order={4} color="white" weight={1000}>{params.gameId}</Title>
          <Button compact variant="outline"
            style={{ marginLeft: '10%', width: '150px' }}
            color={clipboard.copied ? 'teal' : 'blue'}
            onClick={() => clipboard.copy(params.gameId)}>
            {clipboard.copied ? 'Game Id Copied!' : 'Copy Game Id'}
          </Button>
        </div>
        <Space h="md" /> <br />
        <h3>Number of Players</h3>
        <h4 style={{ color: 'grey' }}>{playerNo}</h4>
        <br />
        <h3>Current Round</h3>
        <div style={{ display: 'inline-flex', flexDirection: 'row' }}>
          {gamePaused ? roundBadge('yellow', 'PAUSED') : (round > 0 ? roundBadge('lime', 'Round ' + String(round)) : roundBadge('cyan', 'WARMUP'))}
          <Button compact variant="outline"
            style={{ marginLeft: '10%' }}
            color="indigo"
            radius="md"
            size="md"
            onClick={() => advanceRound()}>
            Advance Round
          </Button>
          {gamePaused
            ? togglePauseButton('green', 'Resume')
            : togglePauseButton('yellow', 'Pause')
          }
        </div>
      </Card>
    </Container>
  )
}

export default Admin
