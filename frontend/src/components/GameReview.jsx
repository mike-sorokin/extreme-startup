import React, { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Table, Title, Card } from '@mantine/core'
import FinalChart from './FinalChart'
import FinalBoard from './FinalBoard'
import { fetchFinalLeaderboard } from '../utils/requests'

function GameReview () {
  const params = useParams()
  const navigate = useNavigate()

  const [finalLeaderboard, setFinalLeaderboard] = useState([])
  const [stats, setStats] = useState({})
  const [keyPoints, setKeyPoints] = useState([])

  // Mock responses
  const mockLeaderboard = [
    {
      player_id: '1',
      name: 'team 1',
      score: 100,
      longest_streak: 10,
      success_ratio: 0.5
    },
    {
      player_id: '2',
      name: 'team 2',
      score: 200,
      longest_streak: 20,
      success_ratio: 0.7
    }
  ]

  const mockChart = {}

  const mockStats = {
    total_requests: 0,
    average_streak: 0, // for streaks at least two correct answers in a row,
    average_on_fire_duration: 0,
    longest_on_fire_duration: {
      achieved_by_team: 0,
      value: 0
    },
    longest_streak: {
      correct_answers_in_a_row: 0,
      duration: 0
    },
    average_success_rate: 0,
    best_success_rate: {
      achieved_by_team: 0,
      value: 0
    },
    most_epic_comeback: {
      achieved_by_team: 0,
      points_gained_during_that_streak: 0,
      duration: 0,
      start_position: 0,
      // in leaderboard
      final_achieved_position: 0
    },
    most_epic_fail: {
      achieved_by_team: 0,
      points_lost_during_that_streak: 0,
      duration: 0,
      start_position: 0,
      final_achieved_position: 0
    }
  }

  const mockKeyPoints = [
    {
      title: 'key point 1',
      description: 'player X beat previous leader and maintained that position for more than 15 seconds',
      occurence_time: 30000,
      achieved_by_team: 'team 2'
    }
  ]

  useEffect(() => {
    const getReviewData = async () => {
      try {
        // Fetch game data here
        const [leaderboardResponse] = await Promise.all([
          fetchFinalLeaderboard(params.gameId)
        ])

        setFinalLeaderboard(leaderboardResponse)
        // setStats(mockStats)
        // setKeyPoints(mockKeyPoints)
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

  return (
    <>
      <h1>Game Review: {params.gameId}</h1>
      <div>
        <h3>Final Chart</h3>
        <FinalChart gameId={params.gameId} players={chartPlayersOfLeaderBoard(finalLeaderboard)} />
      </div>
      <div>
        <h3>Analysis</h3>
        {/* { (Object.entries(stats).length == 0) ? <></> : (
          <ul>
            <li>Total Requests is {stats.total_requests}</li>
            <li>Average Streak is {stats.average_streak}</li>
            <li>Average on Fire Duration {stats.average_on_fire_duration}</li>
            <li>
              Longest on Fire Duration is {stats.longest_on_fire_duration.value}
              and achieved by {stats.longest_on_fire_duration.achieved_by_team}
            </li>
            <li>
              Longest Streak is {stats.longest_streak.correct_answers_in_a_row},
              which lasted for {stats.longest_streak.duration} milliseconds
              and achieved by {stats.longest_streak.achieved_by_team}
            </li>
            <li>Average Success Rate is {stats.average_success_rate}</li>
            <li>
              Best success rate is {stats.best_success_rate.value}
              and achieved by {stats.best_success_rate.achieved_by_team}
            </li>
            <li>
              Most epic comeback was achieved by {stats.most_epic_comeback.achieved_by_team}.
              He or they gained {stats.most_epic_comeback.points_gained_during_that_streak}
              and that bonkers lasted for {stats.most_epic_comeback.duration}.
              {stats.most_epic_comeback.final_achieved_position - stats.most_epic_comeback.start_position}
              was passed, starting from {stats.most_epic_comeback.start_position}
              to {stats.most_epic_comeback.final_achieved_position}
            </li>
            <li>
              Most epic fail was achieved by {stats.most_epic_comeback.achieved_by_team}.
              He or they lost {stats.most_epic_comeback.points_gained_during_that_streak}
              and that bollocks lasted for {stats.most_epic_comeback.duration}.
              {stats.most_epic_comeback.final_achieved_position - stats.most_epic_comeback.start_position}
              was passed, starting from {stats.most_epic_comeback.start_position}
              to {stats.most_epic_comeback.final_achieved_position}
            </li>
          </ul>
        )} */}
      </div>

      <Card sx={{ maxHeight: '200px', overflow: 'auto' }}>
        <Title order={1} color="white" weight={1000}>Final leaderboard</Title>
        <FinalBoard finalBoard={asMappable(finalLeaderboard)} />
      </Card>

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
            mockKeyPoints.map((keyPoint) => (
              <tr key={keyPoint.id}>
                <td>{keyPoint.title}</td>
                <td style={{ width: '300px' }}>{keyPoint.description}</td>
                <td>{keyPoint.occurence_time}</td>
                <td>{keyPoint.acheived_by_team}</td>
              </tr>
            ))
          }
        </tbody>
      </Table>
    </>
  )
}

export default GameReview
