import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Container, Table } from '@mantine/core'

import { fetchFinalStats } from '../utils/requests'

function FinalStats () {
  const params = useParams()
  const [stats, setStats] = useState({})

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
        {
          <Table>
            <thead>
              <tr>
                <th></th>
                <th></th>
              </tr>
            </thead>
            <tbody>

            </tbody>
          </Table>
        }
      </Container>
  )
}

export default FinalStats
