import React, { useState, useEffect } from 'react'
import { Outlet, useParams, useNavigate } from 'react-router-dom'
import { Loader } from '@mantine/core'

import { checkValidGame, checkValidPlayer, checkGameEnded } from './requests'
import { gameReviewUrl } from './urls'
import NotFound from '../components/NotFound'

function ValidRoute () {
  const [loading, setLoading] = useState(true)
  const [valid, setValid] = useState(null)

  const navigate = useNavigate()

  const params = useParams()

  useEffect(() => {

    const checkGameOver = async () => {
      const gameDeletedResponse = await checkGameEnded(params.gameId)
      if (gameDeletedResponse) {
        navigate(gameReviewUrl(params.gameId))
      }
    }

    const validateUrl = async () => {
      // validate game id

      const response = await checkValidGame(params.gameId)

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
    return <Loader />
  }

  // If valid is true, show any child component through Outlet, else show NotFound component
  return (
    valid ? <Outlet /> : <NotFound />
  )
}

export default ValidRoute
