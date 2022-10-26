import React, { useEffect, useState } from 'react'
import { useParams } from "react-router-dom"
import { Container, Table } from "@mantine/core"

import { fetchAllPlayers } from '../utils/requests'

import Chart from "./Chart"

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])

  const params = useParams()

  // Fetches the list of all players and sorts in descending order based on score
  const getLeaderboard = async () => {
    try {
      const response = await fetchAllPlayers(params.gameId)
      const sortedResponse = response.sort((a, b) => { return b.score - a.score })
      setLeaderboard(sortedResponse)
    } catch (error) {
      // TODO
    }
  }

  // Fetches leaderboard data every 2 seconds
  useEffect(() => {
    const timer = setInterval(getLeaderboard, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [])

  return (
    <Container size="xl" px="sm">
      <h2>Leaderboard</h2>
      <Chart gameId={params.gameId} />
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
