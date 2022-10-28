import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@mantine/core'

import { gameUrl } from '../utils/urls'

function GoToGame({ gameId }) {
  const navigate = useNavigate()

  return (
    <div>
      <p>Your game id is: {gameId}</p>
      <Button type="button" onClick={() => { navigate(gameUrl(gameId)) }}>To Game Page</Button>
    </div>
  )
}

export default GoToGame

