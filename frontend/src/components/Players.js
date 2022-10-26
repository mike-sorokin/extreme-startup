import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from "react-router-dom"
import { Button, Container, Table } from '@mantine/core'

import { deleteAllPlayers, deletePlayer, fetchAllPlayers } from '../utils/requests'

function Players() {
  const [players, setPlayers] = useState([])
  const [refreshTimer, setRefreshTimer] = useState(0)

  const params = useParams();
  const navigate = useNavigate();

  // Fetches list of all players
  const getPlayers = async () => {
    try {
      const response = await fetchAllPlayers(params.gameid)
      setPlayers(response)
    } catch (error) {
      // TODO
    }
  }

  // Fetches player data every 2 seconds
  useEffect(() => {
    const timer = setInterval(getPlayers, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [])

  // useEffect(() => {


  //   getPlayers()

  //   setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
  // }, [refreshTimer])

  // useEffect(() => {
  //   getPlayers()
  //   setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
  // }, [refreshTimer]);

  // function getPlayers() {
  //   axios.get(playerCreationUrl(params.gameid))
  //     .then(function (response) {
  //       console.log(response);
  //       const temp = []
  //       for (let [id, player] of Object.entries(response.data.players)) {
  //         temp.push({ 'id': id, 'name': player.name, 'api': player.api })
  //       }
  //       console.log(temp)
  //       setPlayers(temp)
  //       console.log(players)
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  const withdrawPlayer = async (playerId) => {
    try {
      const response = await deletePlayer(params.gameid, playerId)
      console.log(response)
    } catch (error) {
      // TODO
    }
  }

  // function withdrawPlayer(playerid) {
  //   axios.delete("/api" + playerPageUrl(params.gameid, playerid))
  //     .then(function (response) {
  //       console.log(response);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  const withdrawAllPlayers = async () => {
    try {
      const response = await deleteAllPlayers(params.gameid)
      console.log(response)
    } catch (error) {
      // TODO
    }
  }

  // function withdrawPlayers() {
  //   axios.delete(playerCreationUrl(params.gameid))
  //     .then(function (response) {
  //       console.log(response);
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

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
          {players.map((player) => (
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
