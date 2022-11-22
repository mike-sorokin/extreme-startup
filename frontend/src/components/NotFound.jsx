import React from 'react'
import { Card, Stack, Title } from '@mantine/core'

import HomeButton from '../utils/utils'

function NotFound () {
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
        <HomeButton size='lg' />
      </Stack>
    </Card>
  )
}

export default NotFound
