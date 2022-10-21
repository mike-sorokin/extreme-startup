import Container from 'react-bootstrap/Container'
import React, {useEffect, useState} from 'react'
import { useParams } from "react-router-dom"
import Button from 'react-bootstrap/Button'
import Stack from 'react-bootstrap/Stack'
import Table from 'react-bootstrap/Table'
import Modal from 'react-bootstrap/Modal'
import Form from 'react-bootstrap/Form'
import axios from 'axios'
import { requestGameCreation } from '../utils/requests'

function Players() {
    const params = useParams();
    const [players, setPlayers] = useState([])
    const [refreshTimer, setRefreshTimer] = useState(0)
    const [showAddPlayerModal, setShowPlayerModal] = useState(false)
    const [modalName, setModalName] = useState('')
    const [modalAPI, setModalAPI] = useState('')
    const [validated, setValidated] = useState(false);

    useEffect(() => {
        getPlayers()
        setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
      }, [refreshTimer]);

    function getPlayers() {
        axios.get("http://127.0.0.1:5000/api/" + params.gameid + '/players')
        .then(function (response) {
          console.log(response);
          const temp = []
          for (let [id, player] of Object.entries(response.data.players)) {
              temp.push({'id': id, 'name': player.name, 'api':player.api})
          }
          console.log(temp)
          setPlayers(temp)
          console.log(players)
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayer(playerid) {
        axios.delete("http://127.0.0.1:5000/api/" + params.gameid + '/players/' + playerid)
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function withdrawPlayers() {
        axios.delete("http://127.0.0.1:5000/api/" + params.gameid + '/players')
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function addPlayer() {
        var bodyData = new FormData()
        bodyData.append('name', modalName)
        bodyData.append('api', modalAPI)
        axios.post("http://127.0.0.1:5000/api/" + params.gameid + '/players', bodyData)
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    }

    function handleSubmit(event) {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
    
        setValidated(true);

        addPlayer();
        setShowPlayerModal(false);
        setModalName('')
        setModalAPI('')
        setValidated(false)
      };
  
    return (
      <Container className="p-5">

        <Modal show={showAddPlayerModal} onHide={() => setShowPlayerModal(false)}>
            <Modal.Header closeButton>
                <Modal.Title>Join The Game</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <Container>
                <Form noValidate validated={validated} onSubmit={handleSubmit}>
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
            </Modal.Body>

            <Modal.Footer>
                <Button variant="primary" onClick={(event) => handleSubmit(event)}>Join</Button>
            </Modal.Footer>
        </Modal>


          <Stack direction="horizontal" gap={2}>
            <Stack>
                <h3>Players</h3>
            </Stack>
            <Button variant="outline-primary" onClick={() => setShowPlayerModal(true)}>Add Player</Button>
            <Button variant="outline-danger" onClick={() => withdrawPlayers()}>Withdraw All</Button>
          </Stack>
          <hr/>

          <Table>
            <thead>
                <tr>
                <th>ID</th>
                <th>Name</th>
                <th>API</th>
                <th>ACTION</th>
                </tr>
            </thead>
            <tbody>
                {
                    players.map(({name, api, id}) => (
                        <tr>
                        <td>{id}</td>
                        <td>{name}</td>
                        <td>{api}</td>
                        <td><Button variant="outline-danger" onClick={() => withdrawPlayer(id)}>Withdraw</Button></td>
                        </tr>
                    ))
                }
            </tbody>
            </Table>
      </Container>
    )
  }

  export default Players