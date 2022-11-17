import React, { useState, useEffect } from 'react'
import { Card, Container, Space, Table, Title } from '@mantine/core'

function FinalBoard ({ finalBoard }) {
  const [sortedBoard, setSortedBoard] = useState([])

  useEffect(() => {
    const sorted = finalBoard?.sort((a, b) => { return b.score - a.score })
    setSortedBoard(sorted)
  }, [finalBoard])

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
              { sortedBoard && sortedBoard.length >= 1 &&
                <tr style={{ backgroundColor: 'gold' }}>
                  <td>{sortedBoard[0].player_id}</td>
                  <td>{sortedBoard[0].name}</td>
                  <td>{sortedBoard[0].score}</td>
                  <td>{sortedBoard[0].success_ratio}</td>
                  <td>{sortedBoard[0].longest_streak}</td>
                </tr>
              }
              { sortedBoard && sortedBoard.length >= 2 &&
                <tr style={{ backgroundColor: 'silver' }}>
                  <td>{sortedBoard[1].player_id}</td>
                  <td>{sortedBoard[1].name}</td>
                  <td>{sortedBoard[1].score}</td>
                  <td>{sortedBoard[1].success_ratio}</td>
                  <td>{sortedBoard[1].longest_streak}</td>
                </tr>
              }
              { sortedBoard && sortedBoard.length >= 3 &&
                <tr style={{ backgroundColor: 'brown' }}>
                  <td>{sortedBoard[2].player_id}</td>
                  <td>{sortedBoard[2].name}</td>
                  <td>{sortedBoard[2].score}</td>
                  <td>{sortedBoard[2].success_ratio}</td>
                  <td>{sortedBoard[2].longest_streak}</td>
                </tr>
              }
              {
                sortedBoard?.slice(3).map((player) => (
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
