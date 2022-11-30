import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Badge, Button, Card, Container, Group, Space, Stack, Switch, Text, Title } from '@mantine/core'
import { useClipboard } from '@mantine/hooks'

import { fetchGame, updateAutoRoundAdvance, updateGame } from '../utils/requests'
import { showInfoNotification } from '../utils/utils'
import { gameReviewUrl, homeUrl } from '../utils/urls'
import usePrevious from '../utils/hooks/usePrevious'

import ConfirmationModal from '../utils/ConfirmationModal'

function Admin () {
  const [playerNo, setPlayerNo] = useState(0)
  const [round, setRound] = useState(0)
  const [maxRound, setMaxRound] = useState(0)
  const [gamePaused, setGamePaused] = useState(false)
  const [openedEndGame, setOpenedEndGame] = useState(false)
  const [teamsNeedingHelp, setTeamsNeedingHelp] = useState([])
  const [teamsBeingHelped, setTeamsBeingHelped] = useState([])
  const prevList = usePrevious(teamsNeedingHelp)
  const [autoAdvance, setAutoAdvance] = useState(false)

  const params = useParams()
  const navigate = useNavigate()
  const clipboard = useClipboard({ timeout: 500 })

  // Fetches game data every 2 seconds (current round and number of players)
  useEffect(() => {
    const getGameData = async () => {
      let response
      try {
        response = await fetchGame(params.gameId)
      } catch (error) {
        showInfoNotification('Game Abandoned', 'An admin has ended the game with no players.')
        navigate(homeUrl())
      }
      try {
        const notifyAdvance = autoAdvance && response.round > round
        if (notifyAdvance) {
          showInfoNotification('Current Round: ' + response.round, 'The round has been automatically advanced')
        }
        setRound(response.round)
        setMaxRound(response.max_round)
        setGamePaused(response.paused)
        setPlayerNo(response.players.length)
        setTeamsNeedingHelp(response.players_to_assist.needs_assistance)
        setTeamsBeingHelped(response.players_to_assist.being_assisted)
        setAutoAdvance(response.auto_mode)
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

  useEffect(() => {
    for (const team of teamsNeedingHelp) {
      if (!prevList.includes(team)) {
        showInfoNotification('Assist Teams!', 'There are teams needing assistance!')
        break
      }
    }
  }, [teamsNeedingHelp])

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
      await updateGame(params.gameId, { end: '' })
    } catch (error) {
      // TODO
    } finally {
      setOpenedEndGame(false)
      if (playerNo) {
        navigate(gameReviewUrl(params.gameId))
      } else {
        showInfoNotification('Game Abandoned', 'The game was ended with no players.')
        navigate(homeUrl())
      }
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

  // Send a put request to update which teams are being helped
  const setHelping = async (team) => {
    try {
      await updateGame(params.gameId, { assisting: team })
      setTeamsNeedingHelp(teamsNeedingHelp.filter((value) => { return value !== team }))
      setTeamsBeingHelped([...teamsBeingHelped, team])
    } catch (error) {
      console.error(error)
    }
  }

  // Template helper functions below
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
    <>
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
              radius="md" size="md"
              disabled={autoAdvance || round >= maxRound}
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
            : <></>
          }
        </Card>
      </Container>
      <Space h="lg" />
      {(teamsNeedingHelp.length >= 1 || teamsBeingHelped.length >= 1) &&
        <Container size="xl" px="xs">
        <Title order={2} color="dimmed"> Teams needing assistance </Title>
        <Space h="md" />
        <Card>
          <Stack>
            {teamsNeedingHelp?.map((team) => (
              <Card shadow="sm" p="xs" sx={ (theme) => ({ '&:hover': { backgroundColor: theme.colors.dark[5] } })} key={team}>
                <Group position="apart">
                  <Text sx={{ paddingLeft: '1rem' }}>{team}</Text>
                  <Button variant="light" onClick={() => { setHelping(team) }}>I am helping</Button>
                </Group>
              </Card>
            ))}
            {teamsBeingHelped?.map((team) => (
              <Card shadow="sm" p="xs" sx={ (theme) => ({ '&:hover': { backgroundColor: theme.colors.dark[5] } })} key={team}>
                <Group position="apart">
                  <Text sx={{ paddingLeft: '1rem' }}>{team}</Text>
                  <Button variant="light" color="green" >Being helped!</Button>
                </Group>
              </Card>
            ))}
          </Stack>
        </Card>
      </Container>
      }
    </>
  )
}

export default Admin
