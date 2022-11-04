import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Card, Stack, Title } from '@mantine/core'

import { homeUrl } from '../utils/urls'

function NotFound () {
  const navigate = useNavigate()

  return (
    <Card shadow="sm" p="lg" radius="md" withBorder
      style={{
        backgroundColor: '#2C2E33',
        width: 'fit-content',
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)'
      }}>
      <Stack align="center" spacing="xl">
        <Title order={1} color="white" weight={1000}>Page not found</Title>
        <Button variant="outline" color="yellow" radius="md" size="lg" onClick={() => navigate(homeUrl()) }>Go to Home Page</Button>
      </Stack>
    </Card>
  )
}

export default NotFound
