import React, { useState, useEffect } from 'react'
import { Container, Table } from '@mantine/core'

import { ReactComponent as Gold } from '../assets/gold_medal_icon.svg'
import { ReactComponent as Silver } from '../assets/silver_medal_icon.svg'
import { ReactComponent as Bronze } from '../assets/bronze_medal_icon.svg'

// finalBoard prop should be an array of objects, one for each player
function FinalBoard ({ finalBoard }) {
  const [sortedBoard, setSortedBoard] = useState([])

  useEffect(() => {
    const sorted = finalBoard?.sort((a, b) => { return b.score - a.score })
    setSortedBoard(sorted)
  }, [finalBoard])

  const position = (i) => {
    if (i === 1) return <Gold /> // gold
    if (i === 2) return <Silver /> // silver
    if (i === 3) return <Bronze /> // bronze
    return i + '.'
  }

  return (
      <Container size="xl" px="sm">
        {
          <Table>
            <thead>
              <tr>
                <th>Position</th>
                <th>Name</th>
                <th>Score</th>
                <th>Success Rate</th>
                <th>Longest Streak</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {
                sortedBoard?.map((player, index) => (
                  <tr key={player.player_id}>
                    <td>{position(index + 1)}</td>
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
  )
}

export default FinalBoard
