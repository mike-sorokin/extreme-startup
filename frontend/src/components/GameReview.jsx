import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Table, Title, Card, Grid, Space } from '@mantine/core'
import FinalChart from './FinalChart'
import FinalBoard from './FinalBoard'
import { fetchFinalLeaderboard, fetchFinalStats, fetchFinalAnalysis } from '../utils/requests'

const sampleKeyPoints = 
[
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
  {
    "title": "Lorem Ipsum",
    "description": "(SAMPLE) player X beat previous leader and maintained that position for more than 15 seconds",
    "occurrence_time": 12345,
    "acheived_by_team": "mumbo jumbo",   // possibly redundant, because is menrtioned in description
  },
]

function GameReview() {
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

      } catch (error) {
        console.error(error)
      }
    }

    getReviewData()
    console.log(stats)
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

  const desc_percentage = '40%'

  return (
    <>
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
          <Card sx={{ height: '100%', overflow: 'auto' }}>
            <Title order={1} color="white" weight={1000}>Final leaderboard</Title>
            <Space h='lg' />
            <FinalBoard finalBoard={asMappable(finalLeaderboard)} />
          </Card>
        </Grid.Col>
      </Grid>

      <Grid style={{ maxWidth: '100%' }}>
        <Grid.Col lg={4} md={12}>
          <Card>
            <Title order={1} color="white" weight={1000}>Analysis</Title>
            <Space h='lg' />
          </Card>
        </Grid.Col>

        <Grid.Col lg={8} md={12}>
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
                  asMappable(sampleKeyPoints).map((keyPoint) => (
                    <tr key={keyPoint.id}>
                      <td>{keyPoint.title}</td>
                      <td style={{width: desc_percentage}}>{keyPoint.description}</td>
                      <td>{keyPoint.occurrence_time}</td>
                      <td>{keyPoint.acheived_by_team}</td>
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
