import { gamePageUrl } from '../utils/urls'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons';
import { useNavigate } from 'react-router-dom'

function GoToGame(gameIdGetter) {

  const navigate = useNavigate();

  const goToGamePage = () => {

    navigate(gamePageUrl(gameIdGetter.getGameId()))
  }

  return (
    <div>
      <p>Your game id is: {gameIdGetter.getGameId()}</p>
      <Button type="button" onClick={goToGamePage}>To Game Page</Button>
    </div>
  )
}

export default GoToGame
