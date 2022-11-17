import React, { useState, useEffect } from 'react'
import { Outlet, useNavigate, useParams } from 'react-router-dom'
import { Loader } from '@mantine/core'

import { checkAuth } from '../requests'
import { gameUrl } from '../urls'
import { showErrorNotification } from '../utils'
import NotFound from '../../components/NotFound'

function AdminRoute () {
  const [loading, setLoading] = useState(true)
  const [admin, setAdmin] = useState(null)

  const navigate = useNavigate()
  const params = useParams()

  // Checks session cookie before allowing player to navigate to admin route
  useEffect(() => {
    const checkCookie = async () => {
      const response = await checkAuth(params.gameId)

      // If response.authorized is false, navigate to game page and show error
      if (!response.authorized) {
        setLoading(false)
        showErrorNotification('Error', 'You are not authorized to view the admin page!')
        navigate(gameUrl(params.gameId))
        return
      }

      setAdmin(response.authorized)
      setLoading(false)
    }

    checkCookie()
  }, [])

  // Show loader whilst waiting for authentication check
  if (loading) {
    return <Loader style={{
      width: 'fit-content',
      position: 'absolute',
      left: '50%',
      top: '50%',
      transform: 'translate(-50%, -50%)'
    }}/>
  }

  // If admin is true, show any child component through Outlet, else show NotFound component
  // (not found is currently never shown as we navigate away before we get a chance to show it)
  return (
    admin ? <Outlet /> : <NotFound />
  )
}

export default AdminRoute
