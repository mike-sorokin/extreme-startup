import React, { useEffect, useState } from 'react'
import { useParams } from "react-router-dom"
import { Container, Table } from "@mantine/core"

import { fetchAllPlayers } from '../utils/requests'

import Chart from "./Chart"

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])
  const [refreshTimer, setRefreshTimer] = useState(0)

  const params = useParams()

  // Fetches the list of all players and sorts in descending order based on score
  useEffect(() => {
    const getLeaderboard = async () => {
      try {
        const response = await fetchAllPlayers(params.gameid)
        const sortedResponse = response.sort((a, b) => { return b.score - a.score })
        setLeaderboard(sortedResponse)
      } catch (error) {
        // TODO
      }
    }

    getLeaderboard()
    setTimeout(() => setRefreshTimer(prevState => prevState + 1), 3000)
  }, [refreshTimer]);

  // function getLeaderboard() {
  //   axios.get(gameUrl(params.gameid) + '/leaderboard')
  //     .then(function (response) {
  //       console.log(response);
  //       setLeaderboard(response.data)

  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  // }

  return (
    <Container size="xl" px="sm">
      <h2>Leaderboard</h2>
      <Chart gameId={params.gameid} />
      {
        <Table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {
              leaderboard.map((player) => (
                <tr key={player.id}>
                  <td>{player.id}</td>
                  <td>{player.name}</td>
                  <td>{player.score}</td>
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
