import { gameUrl } from '../utils/urls'
import React from 'react'
import { Button, Space, Title } from '@mantine/core'
import { useNavigate } from 'react-router-dom'

function GoToGame (gameIdGetter) {
  const navigate = useNavigate()

  const goToGamePage = () => {
    navigate(gameUrl(gameIdGetter.getGameId()))
  }

  return (
    <div>
      <Title order={2} color="lime" weight={750}>Your game is ready!</Title>
      <Space h="xl" />
      <Title order={5} color="white" weight={500}>Your Game ID is:</Title>
      <Space h="md" />
      <Title order={1} color="white" weight={1000} align="center">{gameIdGetter.getGameId()}</Title>
      <Space h="md" />
      <Button variant="gradient" gradient={{ from: 'teal', to: 'lime', deg: 105 }}
        style={{ marginLeft: '33%' }} onClick={goToGamePage}>To Game Page</Button>
    </div>
  )
}

export default GoToGame
