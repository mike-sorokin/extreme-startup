import React from 'react'
import { Outlet, Navigate } from 'react-router-dom'

function AdminRoute () {
  const auth = { token: false }
  return (
    auth.token ? <Outlet /> : <Navigate to="/" />
  )
}

export default AdminRoute
