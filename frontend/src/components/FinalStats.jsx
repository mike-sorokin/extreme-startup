import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Container, Card, Group, Text, Stack } from '@mantine/core'

import { fetchFinalStats } from '../utils/requests'

function FinalStats () {
  const params = useParams()
  const [stats, setStats] = useState()

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetchFinalStats(params.gameId)
        console.log({ response })
        setStats(response)
      } catch (error) {
        console.error(error)
      }
    }

    fetchStats()
  }, [])

  return (
      <Container size="xl" px="sm">
        { stats && <Stack>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Average Streak:</Text>
                <Text>{Math.round(stats.average_streak)}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Longest Streak:</Text>
                <Text>{stats.longest_streak}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Average Success Rate:</Text>
                <Text>{Math.round(stats.average_success_rate * 100) + '%'}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Best Success Rate:</Text>
                <Text>{Math.round(stats.best_success_rate.value * 100) + '%'}</Text>
                <Text>by</Text>
                <Text>{stats.best_success_rate.team}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Average On Fire duration:</Text>
                <Text>{stats.average_on_fire_duration}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Longest On Fire duration:</Text>
                <Text>{Math.round(stats.longest_on_fire_duration.duration) + 's'}</Text>
                <Text>by</Text>
                <Text>{stats.longest_on_fire_duration.achieved_by_team}</Text>
                <Text>with a streak of</Text>
                <Text>{stats.longest_on_fire_duration.streak_len}</Text>
              </Group>
            </Card>
            <Card shadow="sm" p="xs">
              <Group>
                <Text>Total Requests:</Text>
                <Text>{stats.total_requests}</Text>
              </Group>
            </Card>
          </Stack>}
      </Container>
  )
}

export default FinalStats
