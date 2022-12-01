import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Card, Center, Modal, PasswordInput, Space, Stack, Text, TextInput, Title } from '@mantine/core'

import { checkGameEnded, createNewGame } from '../utils/requests'
import { gameReviewUrl } from '../utils/urls'
import { showErrorNotification, showFailureNotification, showLoadingNotification, updateLoadingNotification } from '../utils/utils'

import AddPlayer from './AddPlayer'
import GoToGame from './GoToGame'

function Home () {
  const navigate = useNavigate()

  const [openedChoosePwd, setOpenedChoosePwd] = useState(false)
  const [openedCreateGame, setOpenedCreateGame] = useState(false)
  const [openedAddPlayer, setOpenedAddPlayer] = useState(false)
  const [openedInfo, setOpenedInfo] = useState(false)
  const [openedReview, setOpenedReview] = useState(false)
  const [gameReviewId, setGameReviewId] = useState('')
  const [newGameId, setNewGameId] = useState('')
  const [pwd, setPwd] = useState('')
  const [creating, setCreating] = useState(false)

  // Creates a new game
  const handleCreateGame = async (event) => {
    event.preventDefault()
    setCreating(true)

    try {
      showLoadingNotification('create-game', 'Game creation in progress', 'Creating game...')
      const response = await createNewGame({ password: pwd })
      updateLoadingNotification('create-game', 'Success!', 'Game successfully created!')
      setNewGameId(response.id)
      setOpenedChoosePwd(false)
      setOpenedCreateGame(true)
    } catch (error) {
      console.error(error)
      if (error.response && error.response.status === 406) {
        console.error('password not sent in request')
      }
      if (error.response && error.response.status === 400) {
        console.error('password cannot be empty')
      }
    } finally {
      setCreating(false)
    }
  }

  const handleGameReview = async (event) => {
    event.preventDefault()
    try {
      console.log(event)
      console.log(gameReviewId)
      // Check game id existed, if so redirect them to a new page with the GameReview component
      const valid = await checkGameEnded(gameReviewId)
      if (valid) {
        navigate(gameReviewUrl(gameReviewId))
      } else {
        showFailureNotification('Error reviewing game', 'You entered an invalid game id!')
      }
    } catch (error) {
      showErrorNotification('Error reviewing game', 'Error searching for game, please try again')
    }
  }

  // Dynamic styling for card to make sure it is not visible once a different modal is open
  const cardStyle = () => {
    const styles = {
      backgroundColor: '#2C2E33',
      width: 'fit-content',
      position: 'absolute',
      left: '50%',
      top: '50%',
      transform: 'translate(-50%, -50%)'
    }

    // Sets visibility to hidden if another modal is open
    if (openedChoosePwd || openedAddPlayer || openedCreateGame || openedInfo || openedReview) {
      styles.display = 'none'
    }

    return styles
  }

  return (
    <div className="Home">
      <Modal centered
        opened={openedChoosePwd}
        onClose={() => setOpenedChoosePwd(false)}
        title="Choose a password"
        withCloseButton={false}>
        <div>
          <form onSubmit={handleCreateGame}>
            <PasswordInput value={pwd} onChange={(e) => setPwd(e.target.value)}
              placeholder="Game password" label="Enter game password:" required data-cy="password-input" />
              <Space h="md" />
            <Button variant="outline" color="green" type="submit" loading={creating}>Create Game!</Button>
          </form>
        </div>
      </Modal>
      <Modal centered
        opened={openedReview}
        onClose={() => setOpenedReview(false)}
        title="Review a Game"
        withCloseButton={false}>
        <div>
          <form onSubmit={handleGameReview}>
            <TextInput value={gameReviewId} onChange={(e) => setGameReviewId(e.target.value)}
              placeholder="Game ID" label="Enter game ID:" required data-cy="game-review-id-input" />
            <Space h="md" />
            <Button variant="outline" color="green" type="submit">Review Game!</Button>
          </form>
        </div>
      </Modal>
      <Modal centered
        opened={openedCreateGame}
        onClose={() => setOpenedCreateGame(false)}
        withCloseButton={false} closeOnClickOutside={false}>
        <GoToGame getGameId={() => newGameId} />
      </Modal>
      <Modal centered size="lg"
        opened={openedAddPlayer}
        onClose={() => setOpenedAddPlayer(false)}
        title="Join a Game!"
        closeOnClickOutside={false}>
        <AddPlayer setOpened={setOpenedAddPlayer} />
      </Modal>
      <Modal centered size="lg"
        opened={openedInfo}
        onClose={() => setOpenedInfo(false)}
        withCloseButton={false} closeOnEscape={false} closeOnClickOutside={false}>
        <div>
          <Text>
            <p>
              Extreme Startup is a software development game / workshop that allows players or teams
              to compete against each other to code and deliver new features, and score points for doing so.
              The game is an interactive learning experience while also being fun and engaging.
              Extreme Startup revolves around the theme of satisfying market demand by encouraging players
              to stay alert and adapt to frequently changing requests for service.
            </p>
          </Text> <Space h="xs" />
          <Text>
            <p>
              The main outline of Extreme Startup is that a number of players deploy an API end-point, register that
              end-point with the game server, and then the game server starts sending them requests. Their
              API end-point should then respond to each request, and if they respond correctly they score points.
              Each game has a number of rounds, where new types of requests are given when the round increments.
              When the game ends, the player / team with the most points wins!
            </p>
          </Text> <Space h="xs" />
          <Text>
            <p>
              In order to play Extreme Startup you will need a pipeline and an API end-point ready to deploy.
              Throughout the game you will be continously developing your API to handle different types of requests.
              Everytime there is a new round, expect new questions!
            </p>
          </Text>
          <Center>
            <Button color="lime" radius="lg" onClick={() => setOpenedInfo(false)}>Got it!</Button>
          </Center>
        </div>
      </Modal>

      <Card shadow="sm" p="lg" radius="md" withBorder sx={cardStyle}>
        <Stack align="center" spacing="xl">
          <Title order={1} color="white" weight={1000}>🔥 Extreme Startup 🔥</Title>
          <Button variant="outline" color="green" radius="md" size="xl" onClick={() => setOpenedAddPlayer(true)}>Join a Game!</Button>
          <Button variant="outline" color="orange" radius="md" size="md" onClick={() => setOpenedChoosePwd(true)}>Create a Game!</Button>
        </Stack>
        <Space h="xl" />
        <div style={{ flexDirection: 'row' }}>
        <Button variant="outline" radius="md" size="xs"
          onClick={() => setOpenedReview(true)} style={{ marginLeft: '12%', width: '125px' }}>
            Review a Game!
        </Button>
        <Button variant="outline" color="pink" radius="xl" size="xs"
          onClick={() => setOpenedInfo(true)} style={{ marginLeft: '8%', width: '125px' }}>
            Learn more
        </Button>
        </div>
      </Card>
    </div>

  )
}

export default Home
