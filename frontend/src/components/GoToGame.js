import { gamePageUrl } from '../utils/urls'
import React from 'react';
import { Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom'

function GoToGame(gameIdGetter) {

  const navigate = useNavigate();

  const goToGamePage = () => {
    navigate(gamePageUrl(gameIdGetter.getGameId()))
  }

  return (
    <div>
      <p>Your game id is: {gameIdGetter.getGameId()}</p>
      <Button color="violet" radius="md" size="md" onClick={goToGamePage}>To Game Page</Button>
    </div>
  )
}

export default GoToGame
