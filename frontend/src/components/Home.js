import React from 'react';
import { useState } from 'react';
import { Button, Card, Modal, Stack, Title } from '@mantine/core';

import AddPlayer from './AddPlayer';
import GoToGame from './GoToGame';

import { requestGameCreation } from '../utils/requests'
import { showSuccessfulNotification } from '../utils/utils'


function Home() {
  const [openedCreateGame, setOpenedCreateGame] = useState(false);
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false);
  const [newGameId, setNewGameId] = useState("")

  const createGameButtonAction = () => {
    return requestGameCreation()
      .then(game => {
        showSuccessfulNotification("Successfully Created Game!")
        setNewGameId(game.id)
        setOpenedCreateGame(true)
      })
  }

  return (
    <div className="Home">
      <Modal centered
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        title="Your game is ready!">
        <GoToGame getGameId={() => newGameId} />
      </Modal>
      <Modal centered
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>

      
      <Card shadow="sm" p="lg" radius="md" withBorder 
            style={{backgroundColor: "#2C2E33", width: "fit-content", 
            position: 'absolute', left: '50%', top: '50%',
            transform: 'translate(-50%, -50%)'}}>
        <Stack align="center" spacing="xl">
          <Title order={1} color="white" weight={1000}>🔥 Extreme Startup 🔥</Title>
          <Button variant="outline" color="green" radius="md" size="lg" onClick={createGameButtonAction}>Create a Game!</Button>
          <Button variant="outline" color="orange" radius="md" size="lg" onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button>
        </Stack>
      </Card>
    </div>
  )
}

export default Home
