import React, { useState, useEffect } from 'react'
import { Outlet, Navigate, useParams } from 'react-router-dom'
import { checkValidGame } from './requests'

function CheckRoute () {
  const [loading, setLoading] = useState(true)
  const [valid, setValid] = useState(true)

  const params = useParams()

  useEffect(() => {
    setLoading(true)
    console.log('loading', loading)
    const validateGame = async () => {
      setValid(await checkValidGame(params.gameId))
    }

    validateGame()
    setLoading(false)
    console.log('loading2', loading)
  }, [])

  return (
    <>
    {!loading && valid ? <Outlet /> : <Navigate to="/"/>}
    </>
  )
}

export default CheckRoute
