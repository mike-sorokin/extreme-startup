import React from 'react'
import { Button, Space, Title } from '@mantine/core'
import { useClipboard } from '@mantine/hooks'
import { useNavigate } from 'react-router-dom'

import { adminUrl } from '../utils/urls'

function GoToGame (gameIdGetter) {
  const navigate = useNavigate()

  const goToGamePage = () => {
    navigate(adminUrl(gameId))
  }

  const clipboard = useClipboard({ timeout: 500 })
  const gameId = gameIdGetter.getGameId()

  return (
    <div>
      <Title order={2} color="lime" weight={750}>Your game is ready!</Title>
      <Space h="xl" />
      <Title order={5} color="white" weight={500}>Your Game ID is:</Title>
      <Space h="md" />
      <Title order={1} color="white" weight={1000} align="center" data-cy='game-id'>{gameId}</Title>
      <Space h="md" />
      <div style={{ flexDirection: 'row' }}>
        <Button variant="outline"
          style={{ marginLeft: '10%', width: '150px' }}
          color={clipboard.copied ? 'teal' : 'blue'}
          onClick={() => clipboard.copy(gameId)}>
          {clipboard.copied ? 'Game Id Copied!' : 'Copy Game Id'}
        </Button>
        <Button variant="gradient"
          style={{ marginLeft: '5%' }}
          gradient={{ from: 'teal', to: 'lime', deg: 105 }}
          onClick={goToGamePage}
          data-cy="to-game-page">To Game Page
        </Button>
      </div>
    </div>
  )
}

export default GoToGame
