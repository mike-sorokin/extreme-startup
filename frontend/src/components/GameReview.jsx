import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Grid, Table, Text, Title } from '@mantine/core'

import FinalChart from './FinalChart'
import FinalBoard from './FinalBoard'
import { fetchFinalLeaderboard, fetchFinalStats, fetchFinalAnalysis } from '../utils/requests'
import HomeButton from '../utils/utils'

function GameReview () {
  const params = useParams()

  const [finalLeaderboard, setFinalLeaderboard] = useState([])
  const [stats, setStats] = useState({})
  const [keyPoints, setKeyPoints] = useState([])
  useEffect(() => {
    const getReviewData = async () => {
      try {
        // Fetch game data here
        const [leaderboardResponse] = await Promise.all([
          fetchFinalLeaderboard(params.gameId)
        ])

        const [analysisResponse] = await Promise.all([
          fetchFinalAnalysis(params.gameId)
        ])

        setFinalLeaderboard(leaderboardResponse)
        setStats(await fetchFinalStats(params.gameId))
        setKeyPoints(analysisResponse)
      } catch (error) {
        console.error(error)
      }
    }

    getReviewData()
    console.log(stats)
    console.log(keyPoints)
  }, [])

  const asMappable = (leaderboard) => {
    if (Array.isArray(leaderboard)) {
      return leaderboard
    } else {
      return Object.keys(leaderboard).map(key => leaderboard[key])
    }
  }

  const chartPlayersOfLeaderBoard = (leaderboard) => {
    return asMappable(leaderboard).map(p => {
      return {
        id: p.player_id,
        name: p.name
      }
    })
  }

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <HomeButton />
      </div>
      <h1>Game Review: {params.gameId}</h1>
      <Grid style={{ maxWidth: '100%' }}>
        <Text>
          {JSON.stringify(stats)}
        </Text>
        <Grid.Col span={8} md={6} lg={8}>
          <Card>
            <Title order={1} color="white" weight={1000}>Final Chart</Title>
            <FinalChart gameId={params.gameId} players={chartPlayersOfLeaderBoard(finalLeaderboard)} />
          </Card>
        </Grid.Col>

        <Grid.Col span={4} md={3} lg={4}>
          <Card sx={{ height: '100%', overflow: 'auto' }}>
            <Title order={1} color="white" weight={1000}>Final leaderboard</Title>
            <FinalBoard finalBoard={asMappable(finalLeaderboard)} />
          </Card>
        </Grid.Col>
      </Grid>

      <div>
        <h3>Analysis</h3>
      </div>
      <h3>Key points</h3>
      <Table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>Occurrence Time</th>
            <th>Player</th>
          </tr>
        </thead>
        <tbody>
          {
            asMappable(keyPoints).map((keyPoint) => (
              <tr key={keyPoint.id}>
                <td>{keyPoint.title}</td>
                <td style={{ width: '300px' }}>{keyPoint.description}</td>
                <td>{keyPoint.time}</td>
                <td>{keyPoint.player_id}</td>
              </tr>
            ))
          }
        </tbody>
      </Table>
    </>
  )
}

export default GameReview
