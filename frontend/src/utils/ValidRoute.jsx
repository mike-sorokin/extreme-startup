import React, { useState, useEffect } from 'react'
import { Outlet, useParams } from 'react-router-dom'
import { Loader } from '@mantine/core'

import { checkValidGame, checkValidPlayer } from './requests'
import NotFound from '../components/NotFound'

function ValidRoute () {
  const [loading, setLoading] = useState(true)
  const [valid, setValid] = useState(null)

  const params = useParams()

  useEffect(() => {
    const validateUrl = async () => {
      // validate game id
      setValid(await checkValidGame(params.gameId))

      // validate player id if necessary
      if (params.id) {
        setValid(await checkValidPlayer(params.gameId, params.id))
      }

      setLoading(false)
    }

    validateUrl()
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

  // If valid is true, show any child component through Outlet, else show NotFound component
  return (
    valid ? <Outlet /> : <NotFound />
  )
}

export default ValidRoute
