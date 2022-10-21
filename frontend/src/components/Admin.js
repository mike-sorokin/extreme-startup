import Container from 'react-bootstrap/Container'
import React, {useEffect, useState} from 'react'
import { useParams } from "react-router-dom"
import Button from 'react-bootstrap/Button'
import Stack from 'react-bootstrap/Stack'
import axios from 'axios'
import { requestGameCreation } from '../utils/requests'

function Admin() {
  const params = useParams();
  const [playerNo, setPlayerNo] = useState(0);
  const [round, setRound] = useState('Warmup')

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/" + params.gameid)
    .then(function (response) {
      console.log(response);
      setRound(response.data.round == 0 ? 'Warmup' : response.data.round)
      setPlayerNo(response.data.players.length)
    })
    .catch(function (error) {
      console.log(error);
    });
  });


  return (
    <Container>
      <Container className='p-5'>
      <h3>Game ID</h3>
      <h4 style={{color: 'grey'}}>{params.gameid}</h4>
      <br />
      <h3>Number of Players</h3>
      <h4 style={{color: 'grey'}}>{playerNo}</h4>
      <br />
    <Stack direction="horizontal" gap={2}>
      <Stack>
        <h3>Rounds</h3>
        <h4 style={{color: 'grey'}}>{round}</h4>
      </Stack>
      <Button variant="outline-secondary">Advance Round</Button>
    </Stack>

    </Container>
    </Container>
  )
}

export default Admin