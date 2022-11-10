import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button, Container, Table, Title } from '@mantine/core'

import { deleteAllPlayers, deletePlayer, fetchAllPlayers } from '../utils/requests'
import { updateSessionData, withCurrentPlayerLiftedIfPresent } from '../utils/utils'

function Players () {
  const [players, setPlayers] = useState([])
  const [isAdmin, setIsAdmin] = useState(false)
  const [playerID, setPlayerID] = useState('')

  const params = useParams()
  const navigate = useNavigate()

  updateSessionData(params.gameId, setIsAdmin, setPlayerID)

  // Fetches player data every 2 seconds
  useEffect(() => {
    const getPlayers = async () => {
      try {
        const players = await fetchAllPlayers(params.gameId)
        console.log("players");
        console.log(players);
        const ordered = withCurrentPlayerLiftedIfPresent(playerID, players)
        console.log("ordered");
        console.log(ordered);
        setPlayers(ordered)
      } catch (error) {
        // Nothing to be done
      }
    }

    getPlayers()
    const timer = setInterval(getPlayers, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId])

  const withdrawPlayer = async playerId => {
    try {
      await deletePlayer(params.gameId, playerId)
      navigate('/' + params.gameId)
    } catch (error) {
      if (error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  const withdrawAllPlayers = async () => {
    try {
      await deleteAllPlayers(params.gameId)
    } catch (error) {
      if (error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  return (
    <Container size="xl" px="sm">
      <Title order={1} color="white" weight={1000}>Players</Title>
      {
        isAdmin
          ? <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button variant="outline" color="red" radius="md" size="md"
                onClick={() => withdrawAllPlayers()}
                data-cy="withdraw-all">Withdraw All
              </Button>
            </div>
          : <></>
      }

      <hr />

      <Table hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>API</th>
            {isAdmin || playerID ? <th>ACTION</th> : <></> }
          </tr>
        </thead>
        <tbody>
          {players.map(player => (
            <tr key={player.id} onClick={() => navigate(player.id)}>
              <td>{player.id}</td>
              <td>{player.name}</td>
              <td>{player.api}</td>
              {
                isAdmin || (player.id === playerID)
                  ? <td>
                      <Button variant="outline" color="red" radius="md" size="md"
                        onClick={() => withdrawPlayer(player.id)}>
                        Withdraw
                      </Button>
                    </td>
                  : <></>
              }
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  )
}

export default Players
