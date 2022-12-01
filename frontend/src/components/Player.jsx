import { React, useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Button, Card, Container, Space, Title } from '@mantine/core'
import { useClipboard } from '@mantine/hooks'

import { fetchPlayer } from '../utils/requests'

import PlayerTable from './PlayerTable'
import useSessionData from '../utils/hooks/useSessionData'

function Player () {
  const [playerData, setPlayerData] = useState({})
  const [events, setEvents] = useState([])

  const clipboard = useClipboard({ timeout: 500 })

  const params = useParams()

  const [isAdmin, playerID] = useSessionData(params.gameId)

  // Fetches player json object from backend
  useEffect(() => {
    const getPlayerData = async () => {
      try {
        const response = await fetchPlayer(params.gameId, params.id)
        setPlayerData(response)
        setEvents(response.events.reverse())
      } catch (error) {
        console.error(error)
      }
    }

    getPlayerData()
    const timer = setInterval(getPlayerData, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId, params.id])

  return (
    <Container size="xl" px="xs">
      <div style={{ display: 'flex' }}>
        <Title order={1} color="white" weight={1000}>Player:</Title>
        <Space w="lg" />
        <Title order={1} color="white" weight={1000}>{playerData.name}</Title>
      </div>
      <Space h="md" />
      <Card shadow="sm" p="lg" radius="md" withBorder>
        <h3>Player ID</h3>
        <h4 style={{ color: 'grey' }} data-cy='player-id'>{playerData.id}</h4>
        <br />
        <h3>Game ID</h3>
        <div style={{ display: 'inline-flex', flexDirection: 'row' }}>
          <Title order={4} color="white" weight={1000} data-cy='game-id'>{playerData.game_id}</Title>
          <Button compact variant="outline"
            style={{ marginLeft: '10%', width: '150px' }}
            color={clipboard.copied ? 'teal' : 'blue'}
            onClick={() => clipboard.copy(playerData.game_id)}>
            {clipboard.copied ? 'Game Id Copied!' : 'Copy Game Id'}
          </Button>
        </div>
        <Space h="md" />
        {isAdmin || (playerData.id === playerID)
          ? <div><br /><h3>API</h3><h4 style={{ color: 'grey' }} data-cy='api'>{playerData.api}</h4></div>
          : <></>}
        <br />
        <h3>Score</h3>
        <Title order={4} color="white" weight={1000} data-cy='score'>{playerData.score}</Title>
        <br />
        <h3>Events</h3>
        <PlayerTable events={events} />
      </Card>
    </Container>
  )
}

export default Player
