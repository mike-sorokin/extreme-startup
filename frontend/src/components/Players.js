import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Button, Container, Table } from '@mantine/core'
import axios from 'axios'
import { useNavigate } from "react-router-dom";
import { playerPageUrl, playerCreationUrl } from '../utils/urls'

import { deleteAllPlayers, deletePlayer, fetchAllPlayers } from '../utils/requests'

function Players () {
  const [players, setPlayers] = useState([])
  const [refreshTimer, setRefreshTimer] = useState(0)
  const params = useParams()
  const navigate = useNavigate()

  const params = useParams()
  const navigate = useNavigate()

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

    function withdrawPlayer(playerid) {
        axios.delete("/api" + playerPageUrl(params.gameid, playerid))
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayers() {
        axios.delete(playerCreationUrl(params.gameid))
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    return (
      <Container size="xl" px="sm">
        <h3>Players</h3>
        <Button variant="gradient" gradient={{ from: 'orange', to: 'red' }}
                radius="md" size="lg" onClick={() => withdrawPlayers()}>Withdraw All</Button>
        <hr/>

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
          {players.map(player => (
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
