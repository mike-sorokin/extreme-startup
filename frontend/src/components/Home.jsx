import React, { useState } from 'react'
import { Button, Modal, Card, Stack, Space, Text, Title, PasswordInput } from '@mantine/core'

import { createNewGame } from '../utils/requests'
import { showSuccessNotification } from '../utils/utils'

import AddPlayer from './AddPlayer'
import GoToGame from './GoToGame'

function Home () {
  const [openedChoosePwd, setOpenedChoosePwd] = useState(false)
  const [openedCreateGame, setOpenedCreateGame] = useState(false)
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false)
  const [openedInfo, setOpenedInfo] = useState(false)
  const [newGameId, setNewGameId] = useState('')
  const [pwd, setPwd] = useState('')

  // Creates a new game
  const handleCreateGame = async (event) => {
    event.preventDefault()
    setOpenedChoosePwd(false)
    setOpenedCreateGame(true)

    try {
      const response = await createNewGame({ password: pwd })
      showSuccessNotification('Successfully Created Game!')
      setNewGameId(response.id)
    } catch (error) {
      // TODO
    }
  }

  return (
    <div className="Home">
      <Modal centered
        opened={openedChoosePwd}
        onClose={() => setOpenedChoosePwd(false)}
        title="Choose a password"
        withCloseButton={false}>
        <div>
          <form onSubmit={handleCreateGame}>
            <PasswordInput value={pwd} onChange={(e) => setPwd(e.target.value)}
              placeholder="Game password" label="Enter game password:" required />
              <Space h="md" />
            <Button variant="outline" color="green" type="submit">Create Game!</Button>
          </form>
        </div>
      </Modal>
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
      <Modal centered
        opened={openedInfo}
        onClose={() => setOpenedInfo(false)}
        withCloseButton={false}>
        <Text>
          Text
        </Text>
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
          <Button variant="outline" color="green" radius="md" size="lg" onClick={() => setOpenedChoosePwd(true)}>Create a Game!</Button>
          <Button variant="outline" color="orange" radius="md" size="lg" onClick={() => setOpenedAddPlayer(true)}>Join a Game!</Button>
          <Button variant="outline" color="pink" radius="xl" onClick={() => setOpenedInfo(true)}>
            About Extreme Startup
          </Button>
        </Stack>
      </Card>
    </div>

  )
}

export default Home
