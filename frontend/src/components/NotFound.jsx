import React from 'react'
import { Link } from 'react-router-dom'

function NotFound () {
  return (
    <>
      <div>Page Not Found</div>
      <Link to="/">Go to Home</Link>
    </>
  )
}

export default NotFound
