import React, { useState } from 'react'
import { Button, Modal } from '@mantine/core'

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
      const response = await createNewGame()
      showSuccessNotification('Successfully Created Game!')
      setNewGameId(response.id)
    } catch (error) {
      // TODO
    }
  }

  return (
    <div className="Home">
      <h1>🔥 Extreme Startup 🔥</h1>
      <Button onClick={handleCreateGame}>Create a Game!</Button>
      <Button onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button>

      <Modal
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        title="Your game is ready!">
        <GoToGame gameId={newGameId} />
      </Modal>
      <Modal
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>
    </div>
  )
}

export default Home
