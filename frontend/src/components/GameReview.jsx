import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Card, Grid, Space, Table, Title } from '@mantine/core'

import FinalChart from './FinalChart'
import FinalBoard from './FinalBoard'
import FinalStats from './FinalStats'
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

        const [statsResponse] = await Promise.all([
          fetchFinalStats(params.gameId)
        ])

        setFinalLeaderboard(leaderboardResponse)
        setStats(statsResponse)
        setKeyPoints(analysisResponse)
        console.log({ analysisResponse })
      } catch (error) {
        console.error(error)
      }
    }

    getReviewData()
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

  const descPercentage = '40%'

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <HomeButton size='md' />
      </div>
      <h1>Game Review: {params.gameId}</h1>
      <Grid style={{ maxWidth: '100%' }}>
        <Grid.Col lg={8} md={12}>
          <Card>
            <Title order={1} color="white" weight={1000}>Final Chart</Title>
            <Space h='lg' />
            <FinalChart gameId={params.gameId} players={chartPlayersOfLeaderBoard(finalLeaderboard)} />
          </Card>
        </Grid.Col>

        <Grid.Col lg={4} md={12}>
          <Card sx={{ maxHeight: '545px', overflow: 'auto' }}>
            <Title order={1} color="white" weight={1000}>Final leaderboard</Title>
            <Space h='lg' />
            <FinalBoard finalBoard={asMappable(finalLeaderboard)} />
          </Card>
        </Grid.Col>

        <Grid.Col lg={6} md={12}>
          <Card sx={{ height: '100%' }}>
            <Title order={1} color="white" weight={1000}>Stats</Title>
            <Space h='lg' />
            <FinalStats />
          </Card>
        </Grid.Col>

        <Grid.Col lg={6} md={12}>
          <Card sx={{ height: '100%', overflow: 'auto' }}>
            <Title order={1} color="white" weight={1000}>Key Points</Title>
            <Space h='lg' />
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
                      <td style={{ width: descPercentage }}>{keyPoint.description}</td>
                      <td>{keyPoint.time}</td>
                      <td>{keyPoint.player_id}</td>
                    </tr>
                  ))
                }
              </tbody>
            </Table>

          </Card>
        </Grid.Col>

      </Grid>
    </>
  )
}

export default GameReview
