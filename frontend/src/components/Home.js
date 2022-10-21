import React from 'react';
import { useState } from 'react';
// import { Container, Modal } from '@mantine/core';
import Button from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Modal from 'react-bootstrap/Modal';
import Table from 'react-bootstrap/Table'
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form'
import Row from 'react-bootstrap/Row';
import AddPlayer from './AddPlayer';
import CreateGame from './CreateGame';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { gameCreationUrl, playerCreationUrl } from '../utils/urls';

function Home() {
  const [showAddPlayer, setShowAddPlayer] = useState(false);
  const navigate = useNavigate();


  const [modalGameId, setModalGameId] = useState('')
  const [modalName, setModalName] = useState('')
  const [modalAPI, setModalAPI] = useState('')

  function handleSubmit(event) {
    addPlayer();
    setShowAddPlayer(false);
    setModalName('')
    setModalAPI('')
    navigate(`/${modalGameId}/players`)
  };

  function addPlayer() {
    var bodyData = new FormData()
    bodyData.append('name', modalName)
    bodyData.append('api', modalAPI)
    axios.post(playerCreationUrl(modalGameId), bodyData)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}
  

  function createNewGame() {
    axios.post(gameCreationUrl())
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
          <Modal.Title>Join a game!</Modal.Title>
        </Modal.Header>
        <Container>
                <Form noValidate onSubmit={handleSubmit}>

                <Form.Group className="mb-3">
                        <Form.Label>Game ID</Form.Label>
                        <Form.Control type="text" value={modalGameId} onChange={(e) => setModalGameId(e.target.value)} required/>
                        <Form.Control.Feedback type="invalid">
                        Please enter a game ID
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Name</Form.Label>
                        <Form.Control type="text" placeholder="Your Name" value={modalName} onChange={e => setModalName(e.target.value)} required/>
                        <Form.Control.Feedback type="invalid">
                        Please enter a name.
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Api</Form.Label>
                        <Form.Control type="text" placeholder="http://...." value={modalAPI} onChange={(e) => setModalAPI(e.target.value)} required/>
                        <Form.Control.Feedback type="invalid">
                        Please enter an API.
                        </Form.Control.Feedback>
                    </Form.Group>
                    </Form>
                </Container>
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
