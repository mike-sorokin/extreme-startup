import React, { useState, useEffect } from 'react'
import { Outlet, useParams, useNavigate } from 'react-router-dom'
import { Button, Center, Loader, Modal, Space, Text } from '@mantine/core'

import { checkValidGame, checkValidPlayer, checkGameEnded } from '../requests'
import { gameReviewUrl } from '../urls'

import NotFound from '../../components/NotFound'

function ValidRoute () {
  const [loading, setLoading] = useState(true)
  const [valid, setValid] = useState(null)
  const [openedGameOver, setOpenedGameOver] = useState(false)

  const navigate = useNavigate()

  const params = useParams()

  useEffect(() => {
    const checkGameOver = async () => {
      const gameDeletedResponse = await checkGameEnded(params.gameId)
      if (gameDeletedResponse) {
        setOpenedGameOver(true)
      }
    }

    const validateUrl = async () => {
      // validate game id
      const response = await checkValidGame(params.gameId)

      // If game id not found then check if the game was ended
      if (!response) {
        checkGameOver()
      }
      setValid(response)

      // validate player id if necessary
      if (params.id) {
        setValid(await checkValidPlayer(params.gameId, params.id))
      }

      setLoading(false)
    }

    validateUrl()
    const interval = setInterval(checkGameOver, 2000)

    return () => {
      clearInterval(interval)
    }
  }, [])

  // Show loader whilst waiting for params check
  if (loading) {
    return <Loader style={{
      width: 'fit-content',
      position: 'absolute',
      left: '50%',
      top: '50%',
      transform: 'translate(-50%, -50%)'
    }}/>
  }

  <Modal centered
      opened={openedGameOver}
      onClose={() => setOpenedGameOver(false)}
      title={'Game Over'} withCloseButton={false}
      closeOnEscape={false} closeOnClickOutside={false}>
      <div>
        <Text>The game has now ended. You can now proceed to the game review page.</Text>
        <Space h="md" />
        <Center>
          <Button variant="filled"
              color="orange"
              radius="md"
              size="md"
              onClick={() => navigate(gameReviewUrl(params.gameId))}>
              Go to Review!
          </Button>
        </Center>
      </div>
  </Modal>

  // If valid is true, show any child component through Outlet, else show NotFound component
  return (
    valid ? <Outlet /> : <NotFound />
  )
}

export default ValidRoute
