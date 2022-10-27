import React from 'react'
import { Table, Badge } from '@mantine/core'

function PlayerTable ({ events }) {
  return (
    <Table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Query</th>
          <th>Difficulty</th>
          <th>Points</th>
          <th>Timestamp</th>
          <th>Outcome</th>
        </tr>
      </thead>
      <tbody>
        {
          events?.map((event) => (
            <tr key={event.id}>
              <td>{event.id}</td>
              <td>{event.query}</td>
              <td>{event.difficulty}</td>
              <td>{event.points_gained}</td>
              <td>{event.timestamp}</td>
              <td>
                {event.response_type === 'NO_RESPONSE' && (
                  <Badge color="red"> NO RESPONSE </Badge>
                )}
                {event.response_type === 'WRONG' && (
                  <Badge color="orange"> INCORRECT </Badge>
                )}
                {event.response_type === 'CORRECT' && (
                  <Badge color="green"> CORRECT </Badge>
                )}
              </td>
            </tr>
          ))
        }
      </tbody>
    </Table>
  )
}

export default PlayerTable
