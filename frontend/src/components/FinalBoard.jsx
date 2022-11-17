import React from 'react'
import { Card, Container, Space, Table, Title } from '@mantine/core'

function FinalBoard ({ finalBoard }) {
  return (
    <Card sx={{ maxHeight: '200px', overflow: 'auto' }}>
      <Container size="xl" px="sm">
        <Title order={1} color="white" weight={1000}>Leaderboard</Title>
        <br />
        <Space h='xl' /> <br />
        {
          <Table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Score</th>
                <th>Success Rate</th>
                <th>Longest Streak</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {
                finalBoard?.map((player) => (
                  <tr key={player.player_id}>
                    <td>{player.player_id}</td>
                    <td>{player.name}</td>
                    <td>{player.score}</td>
                    <td>{player.success_ratio}</td>
                    <td>{player.longest_streak}</td>
                  </tr>
                ))
              }
            </tbody>
          </Table>
        }
      </Container>
    </Card>
  )
}

export default FinalBoard
