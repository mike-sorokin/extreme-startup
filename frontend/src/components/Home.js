import React, { useState } from 'react'
import { Button, Modal, Card, Stack, Title } from '@mantine/core'

import { createNewGame } from '../utils/requests'
import { showSuccessNotification } from '../utils/utils'

import AddPlayer from './AddPlayer'
import GoToGame from './GoToGame'

function Home () {
  const [openedCreateGame, setOpenedCreateGame] = useState(false)
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false)
  const [newGameId, setNewGameId] = useState('')

  // Creates a new game
  const handleCreateGame = async () => {
    setOpenedCreateGame(true)

    try {
      const response = await createNewGame({ password: 'password123' })
      showSuccessNotification('Successfully Created Game!')
      setNewGameId(response.id)
    } catch (error) {
      // TODO
    }
  }

  return (
<div className="Home">
      <Modal centered
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        withCloseButton={false}>
        <GoToGame getGameId={() => newGameId} />
      </Modal>
      <Modal centered size="lg"
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>

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
          <Title order={1} color="white" weight={1000}>🔥 Extreme Startup 🔥</Title>
          <Button variant="outline" color="green" radius="md" size="lg" onClick={handleCreateGame}>Create a Game!</Button>
          <Button variant="outline" color="orange" radius="md" size="lg" onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button>
        </Stack>
      </Card>
    </div>

  )
}

export default Home
