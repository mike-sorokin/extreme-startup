import axios from 'axios';
import React from 'react';
import { useState } from 'react';
import { TextInput, Button } from '@mantine/core';
import { showNotification } from '@mantine/notifications';
import { IconCheck, IconX } from '@tabler/icons';

import AddPlayer from './AddPlayer';
import CreateGame from './components/CreateGame';

function Home() {
  const [openedCreateGame, setOpenedCreateGame] = useState(false);
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false);

  return(
    <div className="Home">
      <Modal
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        title="Create a Game!">
        <CreateGame setOpened={setOpenedCreateGame}/>
      </Modal>
      <Modal
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!">
        <AddPlayer setOpened={setOpenedAddPlayer}/>
      </Modal>

      <h1>Home</h1>
    </div>
  )
}

export default Home