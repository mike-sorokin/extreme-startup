import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { Button, Modal } from '@mantine/core';

import AddPlayer from './AddPlayer';
import CreateGame from './CreateGame';

<<<<<<< HEAD
function Home() {
  const [openedCreateGame, setOpenedCreateGame] = useState(false);
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false);

  return (
    <div className="Home">
      <Modal
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        title="Create a Game!">
        <CreateGame setOpened={setOpenedCreateGame} />
      </Modal>
      <Modal
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>

      <h1>🔥 Extreme Startup 🔥</h1>
      <Button onClick={() => { setOpenedCreateGame(true) }}>Create a Game!</Button>
      <Button onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button>
    </div>
  )
}

export default Home