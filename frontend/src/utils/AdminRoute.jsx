import React, { useState, useEffect } from 'react'
import { Outlet, useNavigate, useParams } from 'react-router-dom'
import { Loader } from '@mantine/core'

import { checkAuth } from './requests'
import { showErrorNotification } from './utils'
import NotFound from '../components/NotFound'

function AdminRoute () {
  const [loading, setLoading] = useState(true)
  const [admin, setAdmin] = useState(null)

  const navigate = useNavigate()
  const params = useParams()

  useEffect(() => {
    const checkCookie = async () => {
      const response = await checkAuth(params.gameId)

      if (!response.authorized) {
        setLoading(false)
        navigate('/' + params.gameId)
        showErrorNotification('Error', 'Not authorised')
      }

      setAdmin(response.authorized)
      setLoading(false)
    }

    checkCookie()
  }, [])

  if (loading) {
    return <Loader />
  }

  return (
    admin ? <Outlet /> : <NotFound />
  )
}

export default AdminRoute
