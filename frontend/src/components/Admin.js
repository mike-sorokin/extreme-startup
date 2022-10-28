import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Button, Container } from '@mantine/core'

import { fetchGame, updateGame } from '../utils/requests'

import '../styles/Admin.css'

function Admin () {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)
  const [gamePaused, setGamePaused] = useState(false)

  const params = useParams()

  // Fetches game data every 2 seconds (current round and number of players)
  useEffect(() => {
    const getGameData = async () => {
      try {
        const response = await fetchGame(params.gameId)
        setRound(response.round)
        setPlayerNo(response.players.length)
      } catch (error) {
        // TODO
      }
    }

    const timer = setInterval(getGameData, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId])

  // Increments round
  const advanceRound = async () => {
    try {
      await updateGame(params.gameId, { round: round + 1 })
      setRound(round + 1)
    } catch (error) {
      // TODO
    }
  }

  // Send a {"pause": ""} request to unpause, {"pause": "p"} to pause
  const togglePauseRound = async () => {
    try {
      const response = await updateGame(params.gameId, { pause: (gamePaused ? '' : 'p') })
      console.log(response)
      setGamePaused(!gamePaused)
    } catch (error) {
      // TODO
    }
  }

  return (
    <Container size="xl" px="xs">
      <h3>Game ID</h3>
      <h4 className="grey-text">{params.gameId}</h4>
      <br />
      <h3>Number of Players</h3>
      <h4 className='grey-text'>{playerNo}</h4>
      <br />
      <div className="rounds-bar">
        <div>
          <h3>Rounds</h3>
        </div>
        <Button
          variant="outline"
          color="dark"
          radius="md"
          size="md"
          style={{
            marginLeft: '20px'
          }}
          onClick={() => advanceRound()}
        >
          Advance Round
        </Button>
                <Button variant="outline"
          color="red"
          radius="md"
          size="md"
          style={{
            marginLeft: '20px'
          }}
          onClick={() => togglePauseRound()}>
          Toggle Pause
        </Button>
      </div>
      <h4 className="grey-text">{round === 0 ? 'Warmup' : round}</h4>
    </Container>
  )
}

export default Admin
