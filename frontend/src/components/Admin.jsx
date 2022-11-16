import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Badge, Button, Card, Container, Space, Switch, Title } from '@mantine/core'
import { useClipboard } from '@mantine/hooks'

import { fetchGame, updateAutoRoundAdvance, updateGame } from '../utils/requests'
import ConfirmationModal from '../utils/ConfirmationModal'
import { showErrorNotification } from '../utils/utils'

function Admin () {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)
  const [gamePaused, setGamePaused] = useState(false)
  const [openedEndGame, setOpenedEndGame] = useState(false)
  const [autoAdvance, setAutoAdvance] = useState(false)

  const params = useParams()
  const clipboard = useClipboard({ timeout: 500 })

  // Fetches game data every 2 seconds (current round and number of players)
  useEffect(() => {
    const getGameData = async () => {
      try {
        const response = await fetchGame(params.gameId)
        if (autoAdvance && response.round > round) {
          showErrorNotification('Round Advancement', 'The round has been automatically advanced')
        }
        setRound(response.round)
        setGamePaused(response.paused)
        setPlayerNo(response.players.length)
      } catch (error) {
        console.error(error)
      }
    }

    getGameData()
    const timer = setInterval(getGameData, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [params.gameId])

  // Increments round
  const advanceRound = async () => {
    try {
      const response = await updateGame(params.gameId, { round: round + 1 })
      if (response === 'ROUND_INCREMENTED') {
        setRound(round + 1)
      }
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  // Toggle automatic round advancement
  const toggleAutoAdvance = async (e) => {
    const isAuto = e.currentTarget.checked
    try {
      const response = await updateAutoRoundAdvance(params.gameId, { auto: isAuto })
      setAutoAdvance(response === 'GAME_AUTO_ON')
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  // Send a {"stop": ""} request to stop the game
  const sendGameEnd = async () => {
    try {
      const response = await updateGame(params.gameId, { end: '' })
      console.log(response)
    } catch (error) {
      // TODO
    } finally {
      setOpenedEndGame(false)
      window.location.reload()
    }
  }

  // Send a {"pause": ""} request to unpause, {"pause": "p"} to pause
  const togglePauseRound = async () => {
    try {
      const response = await updateGame(params.gameId, { pause: (gamePaused ? '' : 'p') })
      setGamePaused(response === 'GAME_PAUSED')
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 401) {
        alert('401 - Unauthenticated request')
      }
    }
  }

  function togglePauseButton (color, text) {
    return <Button compact variant="outline"
      color={color}
      radius="md"
      size="md"
      style={{ marginLeft: '10%', width: '110px' }}
      onClick={() => togglePauseRound()}
      data-cy='pause-game-button'>
      {text}
    </Button>
  }

  function roundBadge (color, text) {
    return <Badge size="xl" color={color} variant="filled"
      style={{ width: '200px' }}
      data-cy='current-round'>
      {text}
    </Badge>
  }

  return (
    <div>
      <ConfirmationModal opened={openedEndGame} setOpened={setOpenedEndGame}
        title='End Game' body='Are you sure you want to end the game?' func={sendGameEnd} />
      <Container size="xl" px="xs">
        <Title order={1} color="white" weight={1000}>Admin Page</Title>
        <Space h="md" />
        <Card shadow="sm" p="lg" radius="md" withBorder>
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <h3>Game ID</h3>
            <div style={{ display: 'flex', marginLeft: '85%' }}>
              <Button compact variant="filled"
                color="red"
                radius="md"
                size="lg"
                onClick={() => setOpenedEndGame(true)}>
                End Game
              </Button>
            </div>
          </div>
          <br />
          <div style={{ display: 'inline-flex', flexDirection: 'row' }}>
            <Title order={4} color="white" weight={1000}>{params.gameId}</Title>
            <Button compact variant="outline"
              style={{ marginLeft: '10%', width: '150px' }}
              color={clipboard.copied ? 'teal' : 'blue'}
              onClick={() => clipboard.copy(params.gameId)}>
              {clipboard.copied ? 'Game Id Copied!' : 'Copy Game Id'}
            </Button>
          </div>
          <Space h="md" /> <br />
          <h3>Number of Players</h3>
          <h4 style={{ color: 'grey' }} data-cy='number-of-players'>{playerNo}</h4>
          <br />
          <h3>Current Round</h3>
          <div style={{ display: 'inline-flex', flexDirection: 'row' }}>
            {gamePaused ? roundBadge('yellow', 'PAUSED') : (round > 0 ? roundBadge('lime', 'Round ' + String(round)) : roundBadge('cyan', 'WARMUP'))}
            <Button compact variant="outline"
              style={{ marginLeft: '10%' }}
              color="indigo"
              radius="md"
              size="md"
              onClick={() => advanceRound()}
              data-cy='advance-round-button'>
              Advance Round
            </Button>
            {gamePaused
              ? togglePauseButton('green', 'Resume')
              : togglePauseButton('yellow', 'Pause')
            }
          </div>
          {round > 0
            ? <Switch
                label="Automatic Round Advancement"
                size="md"
                checked={autoAdvance} onChange={(e) => toggleAutoAdvance(e)}
              />
            : <></>}
        </Card>
      </Container>
    </div>
  )
}

export default Admin
