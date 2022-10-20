import { gamePageUrl } from '../utils/urls'
import { requestGameCreation, requestPlayerCreation, playerCreationData } from '../utils/requests'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';
import { useNavigate } from 'react-router-dom'


function CreateGame(setOpened) {

  const navigate = useNavigate();

  const submission = event => {
    event.preventDefault()
    return requestGameCreation()
      .then(game => {
        // setOpened(false)
        navigate(gamePageUrl(game.id))
      })
  }

  return (
    <div>
      <form onSubmit={submission}>
        <Button type="submit">Create Me</Button>
      </form>
    </div>
  )
}

export default CreateGame
