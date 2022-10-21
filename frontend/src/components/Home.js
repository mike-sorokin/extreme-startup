import React from 'react';
import { useState } from 'react';
import { Button, Modal } from '@mantine/core';

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
      <Modal
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        title="Your game is ready!">
        <GoToGame getGameId={() => newGameId} />
      </Modal>
      <Modal
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>

      <h1>🔥 Extreme Startup 🔥</h1>
      <Button onClick={createGameButtonAction}>Create a Game!</Button>
      <Button onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button>
    </div>
  )
}

export default Home
