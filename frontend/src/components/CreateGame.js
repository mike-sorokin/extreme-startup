import { gamePageUrl } from '../utils/urls'
import { requestGameCreation } from '../utils/requests'
import { showSuccessfulNotification } from '../utils/utils'
import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons';
import { useNavigate } from 'react-router-dom'

function CreateGame(setOpened) {

  const navigate = useNavigate();

  const submission = event => {
    event.preventDefault()
    return requestGameCreation()
      .then(game => {
        showSuccessfulNotification("Successfully Created Game!")
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
