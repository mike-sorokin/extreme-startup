import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Badge, ColorSwatch, Container, Group, Table, Title } from '@mantine/core'

import { fetchAllPlayers } from '../utils/requests'

import Chart from './Chart'

function Leaderboard () {
  const [leaderboard, setLeaderboard] = useState([])

  const params = useParams()

  // Fetches list of all players every 2 seconds and sorts in descending order based on score
  useEffect(() => {
    const getLeaderboard = async () => {
      try {
        const response = await fetchAllPlayers(params.gameId)
        const sortedResponse = response.sort((a, b) => { return b.score - a.score })
        setLeaderboard(sortedResponse)
      } catch (error) {
        // TODO
      }
    }

    const timer = setInterval(getLeaderboard, 2000)
    getLeaderboard()
    return () => {
      clearInterval(timer)
    }
  }, [params.gameId])

  function createBadge (ch) {
    if (ch === '1') {
      return <ColorSwatch color="green"/>
    } else if (ch === '0') {
      return <ColorSwatch color="red"/>
    } else {
      return <ColorSwatch color="orange"/>
    }
  }

  return (
    <Container size="xl" px="sm">
      <Title order={1} color="white" weight={1000}>Leaderboard</Title>
      <Chart gameId={params.gameId} />
      {
        <Table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Recent events</th>
              <th>Score</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {
              leaderboard.map((player) => (
                <tr key={player.id}>
                  <td>{player.id}</td>
                  <td>{player.name}</td>

                  <td><Group position="right" spacing="xs">
                  {[...player.streak].map(createBadge)}
                  </Group>
                  </td>

                  <td>{player.score}</td>
                  <td>{player.streak === '111111' && (<Badge variant="gradient" gradient={{ from: 'orange', to: 'red' }}> ON FIRE! </Badge>)}</td>
                </tr>
              ))
            }
          </tbody>
        </Table>
      }
    </Container>
  )
}

export default Leaderboard
