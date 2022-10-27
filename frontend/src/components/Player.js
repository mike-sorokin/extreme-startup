import { React, useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Container } from '@mantine/core'

import { fetchPlayer } from '../utils/requests'

import PlayerTable from './PlayerTable'

function Player () {
  const [playerData, setPlayerData] = useState({})
  const [events, setEvents] = useState([])

  const params = useParams()

  // Fetches player json object from backend
  useEffect(() => {
    const getPlayerData = async () => {
      try {
        const response = await fetchPlayer(params.gameId, params.id)
        setPlayerData(response)
        setEvents(response.events.reverse())
      } catch (error) {
        // TODO
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
      <PlayerTable events={events} />
    </Container>
  )
}

export default Player
