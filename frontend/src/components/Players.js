import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from "react-router-dom"
import { Button, Container, Table } from '@mantine/core'

import { deleteAllPlayers, deletePlayer, fetchAllPlayers } from '../utils/requests'
import { playersAsArray } from '../utils/utils'

function Players() {
  const [players, setPlayers] = useState([])

  const params = useParams();
  const navigate = useNavigate();

  // Fetches player data every 2 seconds
  useEffect(() => {
    const getPlayers = async () => {
      try {
        const players = await fetchAllPlayers(params.gameId)
        setPlayers(players)
      } catch (error) {
        // TODO
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
      const response = await deletePlayer(params.gameId, playerId)
      console.log(response)
    } catch (error) {
      // TODO
    }
  }

  const withdrawAllPlayers = async () => {
    try {
      const response = await deleteAllPlayers(params.gameId)
      console.log(response)
    } catch (error) {
      // TODO
    }
  }

  return (
    <Container size="xl" px="sm">
      <h3>Players</h3>
      <Button variant="outline" color="red" radius="md" size="md"
        onClick={() => withdrawAllPlayers()}>Withdraw All</Button>
      <hr />

      <Table hover>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>API</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          {players.map( player => (
            <tr key={player.id} onClick={() => navigate(player.id)}>
              <td>{player.id}</td>
              <td>{player.name}</td>
              <td>{player.api}</td>
              <td>
                <Button variant="outline" color="red" radius="md" size="md"
                  onClick={() => withdrawPlayer(player.id)}>
                  Withdraw
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </Container>
  )
}

export default Players
