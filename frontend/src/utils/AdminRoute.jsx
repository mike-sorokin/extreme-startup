import React from 'react'
import { Outlet, Navigate } from 'react-router-dom'

function AdminRoute () {
  const valid = true
  return (
    valid ? <Outlet /> : <Navigate to="/" />
  )
}

export default AdminRoute
