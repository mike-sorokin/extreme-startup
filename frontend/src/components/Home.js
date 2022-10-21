import React from 'react';
import { useState } from 'react';
// import { Container, Modal } from '@mantine/core';
import Button from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Modal from 'react-bootstrap/Modal';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import AddPlayer from './AddPlayer';
import CreateGame from './CreateGame';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

function Home() {
  const [showAddPlayer, setShowAddPlayer] = useState(false);
  const navigate = useNavigate();

  function createNewGame() {
    axios.post('http://127.0.0.1:5000/api')
    .then(function (response) {
      console.log(response);
      const game_id_path = '/' + response.data.id;
      navigate(game_id_path)
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  return (
    // <div className="Home">
      /* <Modal
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
      </Modal> */

      
      // /* <Button variant="primary" onClick={() => { setOpenedCreateGame(true) }}>Create a Game!</Button>
      // <Button variant="primary" onClick={() => { setOpenedAddPlayer(true) }}>Join a Game!</Button> */
    // </div>

    <>

      <Modal show={showAddPlayer} onHide={() => setShowAddPlayer(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Join A Game</Modal.Title>
        </Modal.Header>
        <Modal.Body>Woohoo, you're reading this text in a modal!</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary">
            Submit
          </Button>
        </Modal.Footer>
      </Modal>

      <Stack gap={4} className="p-5">
        <h1 className="text-center">🔥 Extreme Startup 🔥</h1>
        <Stack gap={3} className="col-md-3 mx-auto">
          <Button variant="primary" onClick={createNewGame}>Create a Game</Button>
          <Button variant="primary" onClick={() => {setShowAddPlayer(true)}}>Join a Game</Button>
        </Stack>
      </Stack>
    </>
  )
}

export default Home
