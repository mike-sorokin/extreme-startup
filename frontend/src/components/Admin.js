import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Button, Container } from '@mantine/core'
import axios from 'axios'
import { gameUrl } from '../utils/urls'

function Admin () {
  const params = useParams()
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState('Warmup')
  const [refreshTimer, setRefreshTimer] = useState(0)

  useEffect(() => {
    axios.get(gameUrl(params.gameid))
      .then(function (response) {
        console.log(response)
        setRound(response.data.round === 0 ? 'Warmup' : response.data.round)
        setPlayerNo(response.data.players.length)
      })
      .catch(function (error) {
        console.log(error)
      })

    setTimeout(() => setRefreshTimer(prevState => prevState + 1), 1000)
  }, [refreshTimer])

  function advanceRound () {
    axios.put(gameUrl(params.gameid))
      .then(function (response) {
        console.log(response)
        setRound(round === 'Warmup' ? 1 : (round + 1))
      })
      .catch(function (error) {
        console.log(error)
      })
  }

  const roundsBarStyle = {
    width: '100%',
    display: 'inline-flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center'
  }

  return (
    <Container size="xl" px="xs">
      <h3>Game ID</h3>
      <h4 style={{ color: 'grey' }}>{params.gameid}</h4>
      <br />
      <h3>Number of Players</h3>
      <h4 style={{ color: 'grey' }}>{playerNo}</h4>
      <br />
      <div style={roundsBarStyle}>
        <div>
          <h3>Rounds</h3>
        </div>
        <Button variant="outline"
          color="dark"
          radius="md"
          size="md"
          style={{
            marginLeft: '20px'
          }}
          onClick={() => advanceRound()}>
          Advance Round
        </Button>
      </div>
      <h4 style={{ color: 'grey' }}>{round}</h4>
    </Container>
  )
}

export default Admin
