import React from 'react'
import { Badge, Table } from '@mantine/core'

function PlayerTable ({ events }) {
  return (
    <Table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Query</th>
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
              <td>{event.points_gained}</td>
              <td>{event.timestamp_nice}</td>
              <td>
                {(event.response_type === 'NO_SERVER_RESPONSE' ||
                  event.response_type === 'ERROR_RESPONSE') && (
                  <Badge color="yellow"> NO RESPONSE </Badge>
                )}
                {event.response_type === 'WRONG' && (
                  <Badge color="red"> INCORRECT </Badge>
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
